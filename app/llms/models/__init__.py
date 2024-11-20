import os

from .azure_openai import create_model as create_azure_openai_model
from .litellm import create_model as create_litellm_model


def get_model_from_env():
    model_provider = os.environ.get("MODEL_PROVIDER", "azure_openai")
    return get_model(model_provider)


def get_model(model_provider, **kwargs):
    if model_provider == "azure_openai":
        return create_azure_openai_model(**kwargs)
    elif model_provider == "litellm":
        return create_litellm_model(**kwargs)
    else:
        raise ValueError(f"Unknown model provider {model_provider}")
