from typing import List, Dict

def build_prompt(user_input: str) -> str:
    return f"Answer the following question concisely:\n{user_input}"

# def build_qa_prompt(question: str, hits: List[Dict]) -> str:
#     """
#     검색 결과(hits)만 근거로 답변하도록 지시하는 시스템 프롬프트를 만듭니다.
#     hits: [{"doc_id":..., "score":..., "text":...}, ...]
#     """
#     if not hits:
#         # LLM을 호출하지 않을 때 사용. (qa.py에서 체크)
#         return ""

#     context_blocks = [f"[{i+1}] {h['text']}" for i, h in enumerate(hits)]
#     context = "\n\n".join(context_blocks)

#     return f"""
# 다음은 ‘참고 문단’입니다. 반드시 이 범위 안의 정보만으로 질문에 답하세요.
# 답변에 근거가 없다면 “잘모르겠습니다”라고만 쓰세요.

# 질문: {question}

# 참고 문단:
# {context}

# 규칙:
# 1. 문단 밖 지식을 절대 사용하지 마세요.
# 2. 답변이 끝나면 아래 형식으로 근거를 표시하세요.

# ---
# 참고 문단:
# [1] …
# [2] …
# """.strip()

def build_qa_prompt(question: str, hits: list[dict]) -> str:
    """
    청크 내부 정보만으로 답변하라고 지시하되,
    더 이상 '참고 문단:' 블록을 요구하지 않습니다.
    """
    context = "\n\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))
    return f"""
다음 ‘참고 문단’ 안의 내용만 활용해 질문에 답하세요.
참고 문단 밖의 지식보다 이 범위 안의 정보가 더 중요합니다.
답변과 간단한 설명 및 부가 정보만 출력하세요. 근거 인용·참고 문단 표기는 하지 않습니다.

질문: {question}

참고 문단:
{context}
""".strip()