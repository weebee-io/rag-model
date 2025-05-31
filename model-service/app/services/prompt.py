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


def build_keyword_extraction_prompt(full_text: str) -> str:
    return f"""
    너는 금융과 경제 전문 AI야. 아래의 문제와 보기 또는 뉴스 내용에서 금융이나 경제와 관련된 주요 키워드만 쉼표로 나열해서 추출해줘.
    - 다른 설명은 하지 마
    - 예: '기준금리, 통화량, 환율'

    질문과 보기:
    {full_text}
    """


def build_news_summary_prompt(content: str, keywords: List[str]) -> str:
    """
    뉴스 기사 요약 및 키워드 설명 요청 프롬프트.
    """
    keyword_str = ", ".join(keywords)
    return f"""
아래 뉴스 기사 내용을 반드시 아래 [출력 형식]에 맞춰 답변해.
다른 말, 설명, 인사, 안내 없이 오직 [출력 형식]만 출력해.

[출력 형식]
요약: <1~2문장으로 간결한 요약>
[키워드1: 개념 설명]
[키워드2: 개념 설명]
...

뉴스 본문:
{content}

추출된 키워드:
{keyword_str}
""".strip()

def build_keyword_explanation_prompt_with_context(keyword: str, context: str) -> str:
    """
    검색 결과(context)를 참고하여 키워드 개념 설명을 생성하는 프롬프트.
    """
    return f"""
아래 참고 문단의 내용을 바탕으로 '{keyword}'의 금융/경제적 개념을 1~2문장으로 간결하게 설명해 주세요.
다른 말, 인사, 안내 없이 아래 형식만 출력하세요.

[출력 형식]
[{keyword}: 간단한 개념 설명]

참고 문단:
{context}
""".strip()

def build_llm_fallback_prompt(keyword: str) -> str:
    """
    검색 결과가 없을 때 키워드 개념 설명을 요청하는 프롬프트.
    """
    return f"""
'{keyword}'는 금융 또는 경제와 관련된 용어입니다.
이 키워드에 대해 1문장으로 개념을 설명해 주세요. 결과는 아래 형식으로만 출력하세요:

[{keyword}: 간단한 개념 설명]
""".strip()


def keyword_prompt(full_text: str) -> str:
    return f"""
    너는 금융과 경제에 특화된 전문 키워드 추출 AI야.

    아래 텍스트에서 '금융' 또는 '경제'와 관련된 전문 용어만 쉼표로 구분해서 추출해.
    - 반드시 **금융 또는 경제 관련 용어**만 포함할 것. (예: '금리', '채권', '환율', '여신', '파킹통장', '인플레이션')
    - 일반 단어, 상황 설명, 인물 이름, 지명, 기관명, '책', '정부' 등 **비금융/비경제 단어는 절대 포함하지 말 것.**
    - 해당 단어가 문맥상 중요해 보여도 **금융·경제 용어가 아니면 무조건 제외**.
    - 결과는 **쉼표로 구분된 키워드 리스트**만 출력 (예: '금리, 환율, 인플레이션')
    - 출력 외에 그 어떤 설명도 하지 마.

    입력 텍스트:
    {full_text}
    """


def build_keyword_explanation(text: str, keyword: str, context: str) -> str:
    """
    검색 결과(context)를 참고하여 키워드 개념 설명을 생성하는 프롬프트.
    """
    return f"""
아래 참고 문단의 내용을 바탕으로 '{keyword}'의 금융/경제적 개념을 1~2문장으로 간결하게 설명해 주세요.
다른 말, 인사, 안내 없이 아래 형식만 출력하세요.

[출력 형식]
[{keyword}: 간단한 개념 설명]

참고 문단:
{context}
""".strip()
def build_news_explanation_prompt(text: str, keyword: str, context: str) -> str:
    """
    검색 결과(context)를 참고하여 키워드 개념 설명을 생성하는 프롬프트.
    """
    return f"""
아래 참고 문단의 내용을 바탕으로 '{keyword}'의 금융/경제적 개념을 1~2문장으로 간결하게 설명해 주세요.
다른 말, 인사, 안내 없이 아래 형식만 출력하세요.

[뉴스]
{text}

[출력 형식]
[{keyword}: 간단한 개념 설명]

참고 문단:
{context}
""".strip()


def build_news_explanation_prompt(text: str, keyword: str, context: str) -> str:
    """
    검색 결과(context)를 참고하여 키워드 개념 설명을 생성하는 프롬프트.
    """
    return f"""
아래 참고 문단의 내용을 바탕으로 '{keyword}'의 금융/경제적 개념을 1~2문장으로 간결하게 설명해 주세요.
다른 말, 인사, 안내 없이 아래 형식만 출력하세요.

[뉴스]
{text}

[출력 형식]
[{keyword}: 간단한 개념 설명]

참고 문단:
{context}
""".strip()

def build_hint_generation_prompt(text: str, keyword: str, context: str) -> str:
    """
    검색 결과(context)를 참고하여 키워드 개념 설명을 생성하는 프롬프트.
    """
    return f"""
아래 참고 문단의 내용을 바탕으로 '{keyword}'의 금융/경제적 개념을 1~2문장으로 간결하게 설명해 주세요.
다른 말, 인사, 안내 없이 아래 형식만 출력하세요.

[뉴스]
{text}

[출력 형식]
[{keyword}: 간단한 개념 설명]

참고 문단:
{context}
""".strip()

