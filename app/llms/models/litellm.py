import os
from langchain_openai import ChatOpenAI


def create_model():
    return ChatOpenAI(
        openai_api_base=os.getenv("LITELLM_API_BASE"),
        openai_api_key=os.getenv("LITELLM_API_KEY"),
        model=os.getenv("LITELLM_MODEL_NAME"),
    )
