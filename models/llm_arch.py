import time
import os
from groq import Groq
from dotenv import load_dotenv
from models.base import BaseModel
from openai import OpenAI

load_dotenv()

class GroqModel(BaseModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, prompt: str) -> dict:
        start = time.time()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        latency_ms = (time.time() - start) * 1000
        output = response.choices[0].message.content

        return {
            "model": self.model_name,
            "output": output,
            "latency_ms": round(latency_ms, 2),
        }
    

class NvidiaModel(BaseModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)

        self.client = OpenAI(
            api_key=os.getenv("NVIDIA_API_KEY"),
            base_url="https://integrate.api.nvidia.com/v1",
            timeout=30
        )

    def generate(self, prompt: str) -> dict:
        start = time.time()

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=512
        )

        latency_ms = (time.time() - start) * 1000

        return {
            "model": self.model_name,
            "output": response.choices[0].message.content,
            "latency_ms": round(latency_ms, 2),
        }