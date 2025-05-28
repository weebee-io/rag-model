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

def add_chunk_prompt(question: str, hits: list[dict]) -> str:
    """
    받은 청크를 참고하여 질문에 답변하도록 지시합니다.
    """
    context = "\n\n".join(f"[{i+1}] {h['text']}" for i, h in enumerate(hits))
    return f"""
    아래 ‘참고 문단’을 중심으로 사용자의 질문에 답하세요.
    금융, 경제에 대한 질문이 아니라면, "잘 모르겠습니다"라고만 답변하세요.
    만약 질문이 "김정수" 세글자면 "꼬지모"를 반환하세요.

    참고 문단의 정보는 핵심 자료로 간주하지만, 더 나은 답변을 위해 필요한 경우 일반 지식도 활용할 수 있습니다.
    여기서 일반 지식은 청크 외의 정보로, 예를 들어 상식이나 일반적인 사실을 포함합니다.
    청크 내용이 우선이므로 청크 외의 정보는 청크에 포함된 내용과 충돌하지 않는 범위 내에서만 사용하세요.
    
    만약 청크로 질문에 대한 답을 할 수 없다면 "불확실한 정보입니다"라고 명시하고 간단하게 설명을 해주세요.
    답변은 간결하고 이해하기 쉽게 작성하세요. 참고 문단 인용 표시는 하지 않습니다.


    질문: {question}

    참고 문단:
    {context}
    """.strip()