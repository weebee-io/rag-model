# dags/jsonl_to_es_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
import os
import glob
import json
import numpy as np  # nan/inf 체크용

# ┌───────────────────────────────────────────────┐
# │ 1. 전역 설정                                   │
# └───────────────────────────────────────────────┘

# Elasticsearch 인덱스명
INDEX_NAME    = "finance_knowledge_chunks"

# JSONL 파일을 모아둘 디렉토리 경로
JSONL_FOLDER  = "/data/"

# EC2에 배포된 Elasticsearch URL
ES_URL        = "http://52.78.209.43:9200/"

# 인증서 검증 여부 (False로 하면 HTTPS 인증서 무시)
VERIFY_CERTS  = False

# ┌───────────────────────────────────────────────┐
# │ 2. DAG 기본 인수                              │
# └───────────────────────────────────────────────┘

DEFAULT_ARGS = {
    "owner":            "finance_team",               # 태스크 소유자
    "depends_on_past":  False,                        # 이전 실행 결과에 의존하지 않음
    "start_date":       datetime(2025, 5, 27),        # 스케줄 시작일
    "retries":          1,                            # 실패 시 재시도 횟수
    "retry_delay":      timedelta(minutes=5),         # 재시도 간격
}

# ┌───────────────────────────────────────────────┐
# │ 3. DAG 정의                                   │
# └───────────────────────────────────────────────┘

with DAG(
    dag_id="jsonl_folder_to_ec2_es",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",  # 매일 한 번 실행
    catchup=False                # 과거 일자 채우기 비활성화
) as dag:

    # ┌─────────────────────────────────────────────┐
    # │ 3-1. 인덱스 생성 Task                        │
    # └─────────────────────────────────────────────┘
    def task_create_index(**context):
        """
        Elasticsearch에 접속하여 INDEX_NAME 인덱스가 존재하지 않으면 생성한다.
        이미 존재할 경우, 기존 매핑의 embedding 차원이 모델 차원과 다르면
        인덱스를 삭제 후 재생성한다.
        """
        # Elasticsearch 클라이언트 초기화 (v11 호환)
        es = Elasticsearch(
            ES_URL,
            verify_certs=VERIFY_CERTS,
            request_timeout=120,
            max_retries=3,
            retry_on_timeout=True
        )
        # SBERT 모델 로딩 및 임베딩 차원 취득
        model = SentenceTransformer("nlpai-lab/KURE-v1")
        MODEL_DIM = model.get_sentence_embedding_dimension()

        # 인덱스가 이미 존재하는지 확인
        if es.indices.exists(index=INDEX_NAME):
            mapping_info = es.indices.get_mapping(index=INDEX_NAME)
            cur_dims = mapping_info[INDEX_NAME]['mappings']['properties']['embedding']['dims']
            if cur_dims != MODEL_DIM:
                print(f"⚠️ 기존 dims({cur_dims}) != 모델 dims({MODEL_DIM}), 인덱스 재생성")
                es.indices.delete(index=INDEX_NAME)
            else:
                print(f"ℹ️ 인덱스 '{INDEX_NAME}' 이미 존재 (dims 일치)")
                return

        # 매핑 정의 (모델 차원에 맞춤)
        mapping = {
            "mappings": {
                "properties": {
                    "chunk_id":       {"type": "keyword"},
                    "page_id":        {"type": "integer"},
                    "title":          {"type": "keyword"},
                    "created_at":     {"type": "date"},
                    "source":         {"type": "keyword"},
                    "overlap_tokens": {"type": "integer"},
                    "text":           {"type": "text",
                                       "analyzer":"nori"},  # analyzer="nori"
                    "embedding": {
                        "type":           "dense_vector",
                        "dims":           MODEL_DIM,
                        "index":          True,
                        "similarity":     "cosine",
                        "index_options": {
                            "type":            "hnsw",
                            "m":               16,
                            "ef_construction": 100
                        }
                    }
                }
            }
        }

        # 인덱스 생성
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"✅ 인덱스 '{INDEX_NAME}' 생성 완료 (dims={MODEL_DIM})")

    # ┌─────────────────────────────────────────────┐
    # │ 3-2. JSONL 폴더 순회 및 업로드 Task           │
    # └─────────────────────────────────────────────┘
    def task_upload_folder(**context):
        """
        JSONL_FOLDER 내의 모든 .jsonl 파일을 찾아,
        레코드를 읽어 임베딩을 생성한 뒤 Elasticsearch에 업로드한다.
        """
        es = Elasticsearch(
            ES_URL,
            verify_certs=VERIFY_CERTS,
            request_timeout=120,
            max_retries=3,
            retry_on_timeout=True
        )
        model = SentenceTransformer("nlpai-lab/KURE-v1")
        MODEL_DIM = model.get_sentence_embedding_dimension()

        # 폴더 내 모든 JSONL 파일 경로 리스트
        pattern = os.path.join(JSONL_FOLDER, "*.jsonl")
        jsonl_files = glob.glob(pattern)

        if not jsonl_files:
            print(f"❌ JSONL 파일이 없습니다: {JSONL_FOLDER}")
            return

        # 각 파일 순회하며 업로드
        for filepath in jsonl_files:
            print(f"📄 업로드 시작: {filepath}")
            actions = []
            filename = os.path.basename(filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    doc = json.loads(line)
                    text = doc.get("text", "")

                    # 임베딩 생성 및 정규화
                    embedding = model.encode(text, normalize_embeddings=True)

                    # 유효성 검사: 차원 불일치, NaN/Inf
                    if (len(embedding) != MODEL_DIM
                        or np.isnan(embedding).any()
                        or np.isinf(embedding).any()):
                        print(f"❌ 잘못된 임베딩 건너뜀 (line {i}, len={len(embedding)})")
                        continue

                    doc["embedding"] = embedding.tolist()
                    unique_id = f"{filename}_{i:05d}"
                    actions.append({
                        "_op_type": "index",
                        "_index":   INDEX_NAME,
                        "_id":      unique_id,
                        "_source":  doc
                    })

                    # 배치 단위로 Bulk 전송
                    if len(actions) >= 500:
                        success, errors = helpers.bulk(
                            es, actions,
                            stats_only=False,
                            raise_on_error=False
                        )
                        print(f"🔄 Batch 업로드: 성공 {success}, 실패 {len(errors)}건")
                        actions.clear()

            # 잔여 액션 전송
            if actions:
                success, errors = helpers.bulk(
                    es, actions,
                    stats_only=False,
                    raise_on_error=False
                )
                print(f"🔄 최종 업로드: 성공 {success}, 실패 {len(errors)}건")

            print(f"✅ 업로드 완료: {filepath}")

    # PythonOperator로 Task 등록
    t1 = PythonOperator(
        task_id="create_index",
        python_callable=task_create_index,
        provide_context=True
    )
    t2 = PythonOperator(
        task_id="upload_folder",
        python_callable=task_upload_folder,
        provide_context=True
    )

    # 실행 순서: 인덱스 생성 → 폴더 업로드
    t1 >> t2
