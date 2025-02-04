from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
import asyncio
from autogen_core import CancellationToken
from dotenv import load_dotenv
import os
import json
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image as RImage
from PIL import Image
 
 
load_dotenv()
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
API_KEY = os.getenv('API_KEY')
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
 
 
Sys_msg = """Can you describe the content of this image and also extract the content in a user readable and organised format?"""

 
 
model_client1 = AzureOpenAIChatCompletionClient(
    azure_deployment=DEPLOYMENT_NAME,
    azure_endpoint=AZURE_ENDPOINT,
    model="gpt-4o",
    api_version=OPENAI_API_VERSION,
    api_key=API_KEY,
)
 
 
async def get_img(path):
    my_img = Image.open(path)
    img = RImage(my_img)
    return img
 
 
async def get_multi_modal_message(query):
    img = await get_img(query)
    return [MultiModalMessage(content=[Sys_msg, img], source="User")]
 
 
async def get_text_content_response(query):
    try:
        multi_modal_message = await get_multi_modal_message(query)
 
        img_analyser = AssistantAgent(
            name="assistant",
            system_message="You are a helpful assistant.",
            model_client=model_client1,
        )
 
        cancellation_token = CancellationToken()
        response = await img_analyser.on_messages(multi_modal_message, cancellation_token)
        data = [{'name':query, 'content':response.chat_message.content, 'status':'true'}]
        return json.dumps(data)
    except Exception as e:
        data = [{'name':query, 'content':str(e), 'status':'false'}]
        return json.dumps(data)
 
 
async def main():
    image_path = r"Image (1).jpg" #image path
    await get_text_content_response(image_path)

if __name__ == "__main__":
    asyncio.run(main())