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

# ─── 1. 전역 설정 ─────────────────────────────────

# Elasticsearch 인덱스명
INDEX_NAME = os.getenv("ES_INDEX_NAME", "finance_knowledge_chunks")
# JSONL 파일을 모아둘 디렉토리 경로
JSONL_FOLDER  = "/data/"
# EC2에 배포된 Elasticsearch URL
ES_URL = os.getenv("ES_URL")
# 인증서 검증 여부
VERIFY_CERTS  = os.getenv("ES_VERIFY_CERTS", "false").lower() == "true"

# ─── 2. DAG 기본 인수 ───────────────────────────────
DEFAULT_ARGS = {
    "owner":           "finance_team",
    "depends_on_past": False,
    "start_date":      datetime(2025, 5, 27),
    "retries":         1,
    "retry_delay":     timedelta(minutes=5),
}

# ─── 3. DAG 정의 ───────────────────────────────────
with DAG(
    dag_id="test_dag",
    default_args=DEFAULT_ARGS,
    # 3분마다 실행하도록 수정
    schedule_interval="*/3 * * * *",
    catchup=False
) as dag:

    def task_create_index(**context):
        # (생략: 기존 인덱스 생성 로직 동일)
        ...

    def task_upload_folder(**context):
        es = Elasticsearch(
            ES_URL,
            verify_certs=VERIFY_CERTS,
            request_timeout=120,
            max_retries=3,
            retry_on_timeout=True
        )
        model = SentenceTransformer("nlpai-lab/KURE-v1")
        MODEL_DIM = model.get_sentence_embedding_dimension()

        # 3분 전 시점으로 cutoff 변경
        cutoff = datetime.now() - timedelta(minutes=3)

        pattern = os.path.join(JSONL_FOLDER, "*.jsonl")
        jsonl_files = glob.glob(pattern)
        new_files = [
            f for f in jsonl_files
            if datetime.fromtimestamp(os.path.getmtime(f)) > cutoff
        ]

        if not new_files:
            print(f"❌ 지난 3분 내 새로운 JSONL 파일 없음 (폴더: {JSONL_FOLDER})")
            return

        # (이후 업로드 로직 동일)
        for filepath in new_files:
            ...
            
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

    t1 >> t2
