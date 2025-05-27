# app/prompts/base.py
from abc import ABC, abstractmethod

class PromptTemplate(ABC):
    @abstractmethod
    def format(self, **kwargs) -> str:
        pass