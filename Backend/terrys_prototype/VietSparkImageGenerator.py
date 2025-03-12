# Import the OpenAI library for interacting with the API
import openai
from dotenv import load_dotenv
import os
load_dotenv()
# Set the OpenAI API key to authenticate requests (replace this with your secure key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a user prompt for image generated link
image_prompt = "Create an image of a vietnamese pho bowl"

image_response = openai.Image.create(
    prompt=image_prompt,
    n=1,
    size="1024x1024"

)
image_url = image_response['data'][0]['url']
print(image_url)