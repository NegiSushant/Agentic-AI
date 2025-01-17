from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
#create the token provider

load_dotenv()
endpoint = os.getenv('AZURE_ENDPOINT')
Api_key = os.getenv('API_KEY')
deployment = os.getenv('DEPLOYMENT_NAME')
vesrion = os.getenv('OPENAI_API_VERSION')



client = AzureOpenAIChatCompletionClient( 
    
    azure_depoyment_id="your_deployment_id",
    model="gpt-4o",
    api_version= vesrion,
    azure_endpoint= endpoint,                                     
    )