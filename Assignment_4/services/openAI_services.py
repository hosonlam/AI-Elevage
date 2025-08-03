import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

def create_client():
    """Create and return Azure OpenAI client."""
    return AzureOpenAI(
        api_version="2023-05-15",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )