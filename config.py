# config.py
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = init_chat_model(
            model=os.getenv("LLM_MODEL", "Qwen/Qwen3-4B"),
            base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8005/v1"),
            api_key=os.getenv("VLLM_API_KEY", "dummy-key"),
            model_provider="openai",
            temperature=0.0,
        )
    return _llm_instance