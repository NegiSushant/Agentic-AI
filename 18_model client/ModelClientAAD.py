from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


#create the token provider
token_pro = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="{deployement}",
    model="gpt-4o",
    api_version="2024-06-01",
    azure_endpoint="https://{..............}.openai.azure.com/",
    azure_ad_token_provider=token_pro
)

