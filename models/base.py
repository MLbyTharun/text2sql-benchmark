from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate(self, prompt: str) -> dict:
        """
        Returns:
        {
            "model": model name,
            "output": generated text,
            "latency_ms": time taken,
        }
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(model={self.model_name})"