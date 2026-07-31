# config.py
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return init_chat_model(
        model=os.getenv("LLM_MODEL", "Qwen/Qwen3-4B"),
        openai_api_base=os.getenv("VLLM_BASE_URL", "http://localhost:8005/v1"),
        openai_api_key=os.getenv("VLLM_API_KEY"),
        model_provider="openai",
        temperature=0.0,
    )