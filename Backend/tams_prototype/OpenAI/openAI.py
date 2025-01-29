from openai import OpenAI
import gradio
from dotenv import load_dotenv
import os
load_dotenv()
# Set the OpenAI API key to authenticate requests (replace this with your secure key)
OAI_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OAI_api_key
)
prompt = f"""
You are a Vietnamese recipe expert. You are only allowed to respond in the form of a JSON. Time should be in minutes. The JSON should always take the following shape:
{{
    "name": " ",
    "ingredients": [{{"ingredientName": "ingredientName", "ingredientAmount": "ingredient amount with unit"}}],
    "calories": " ",
    "time": " ",
    "servings": " ",
    "instructions": ["step 1", "step 2"]
}}
I will provide you a list of ingredients, and you will always respond with your best recommendation for a Vietnamese recipe. Here are the ingredients I have:
{{ingredients}}

Respond only with the JSON format as described above.
"""

# Initialize a message history list with the system prompt
# This structure is required for the OpenAI chat model to maintain context.
messages = [{"role": "system", "content": prompt}]

# Define a function to handle user input and generate a response using OpenAI's API
def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,  # Specify the model to use
        messages = messages       # Pass the conversation history
    )
    ChatGPT_reply = response.choices[0].message.content
    # Add the assistant's reply to the message history to maintain context
    messages.append({"role": "assistant", "content": response})
    return ChatGPT_reply


# Create a Gradio interface with the custom chatbot function
demo = gradio.Interface(
    fn=CustomChatGPT,        # Function to handle chatbot interactions
    inputs="text",           # Input type is plain text
    outputs="text",          # Output type is plain text
    title="VietSpark Chef"   # Title of the Gradio application
)
demo.launch(share=True)

