from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os


load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
Api_key = os.getenv("API_KEY")
apiVersion = os.getenv("OPENAI_API_VERSION")

#create the token provider
# token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")


client = AzureOpenAIChatCompletionClient(
    azure_depoyment_id="gpt-4o",
    model="gpt-4o",
    api_version= apiVersion,
    azure_endpoint=endpoint,
    # AZURE_OPENAI_API_KEY = Api_key
    api_key = Api_key
)