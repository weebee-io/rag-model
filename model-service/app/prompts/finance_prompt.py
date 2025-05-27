# app/prompts/finance_prompt.py
from .base import PromptTemplate

class FinancePrompt(PromptTemplate):
    @staticmethod
    def expansion(question: str) -> str:
        return f"Expand the query for financial context: {question}"

    @staticmethod
    def answer(question: str, contexts: list) -> str:
        context_str = "\n---\n".join(contexts)
        return (
            f"You are an AI assistant specialized in finance. "
            f"Use the following context to answer the question:\n{context_str}\nQuestion: {question}\nAnswer:"
        )
