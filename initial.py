from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

#create the token provider
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")


client = AzureOpenAIChatCompletionClient( 
    token_provider=token_provider,
    azure_depoyment_id="your_deployment_id",
    model="",
    api_version= "",
    azure_endpoint="https://your_endpoint.cognitiveservices.azure.com",                                     
    )