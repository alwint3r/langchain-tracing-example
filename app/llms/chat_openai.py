from langchain_openai import AzureChatOpenAI
import os


def get_model_default():
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_API_BASE"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
