from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
import openai
import aiohttp
import asyncio
import time
import os
from dotenv import load_dotenv


app = FastAPI()

# In-memory backend (session storage)
session_store: Dict[str, str] = {}
q = []

class User(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(user: User):
    # In a real application, you would validate the credentials
    if user.username == "test" and user.password == "password":
        # Simulating session creation with an in-memory backend
        session_token = f"token-{user.username}"
        session_store[session_token] = user.username
        return {"session_token": session_token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.get("/profile/")
async def profile(session_token: str):
    # Check if the session token exists in the in-memory store
    username = session_store.get(session_token)
    if username:
        return {"username": username}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token")

@app.post("/logout/")
async def logout(session_token: str):
    # Invalidate the session by removing it from the in-memory store
    if session_token in session_store:
        del session_store[session_token]
        return {"message": "Logged out successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

@app.get("/timer")
async def count_time(item:str):
    global q
    q.append(item)

    asyncio.create_task(count(q))
    return len(q)

async def count(q):
    while len(q) > 0:
        print(len(q))
        print("sending...")
        repsonse = await call_openai_api(q[0])
        print(repsonse)
        q.pop(0)



# Your OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OAI_API_KEY")

# Define an async function to make API calls to GPT
async def call_openai_api(prompt):
    message = [{"role": "user", "content": prompt}]
    print(f"Calling OpenAI API with prompt: {prompt}")
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Or whichever model you are using
            messages=message,
            max_tokens=100
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred during API call: {str(e)}")
        return None

# Define a worker function to process tasks from the queue
async def worker(queue):
    while True:
        prompt = await queue.get()
        if prompt is None:
            break
        await call_openai_api(prompt)
        queue.task_done()

# Create a main function that runs tasks concurrently using a queue
async def process_multiple_tasks(prompts):
    queue = asyncio.Queue()

    # Create worker tasks to process the queue concurrently
    workers = [asyncio.create_task(worker(queue)) for _ in range(3)]

    # Put all the prompts in the queue
    for prompt in prompts:
        await queue.put(prompt)

    # Wait until the queue is fully processed
    await queue.join()

    # Stop the workers
    for _ in range(3):
        await queue.put(None)
    await asyncio.gather(*workers)

# Driver code
async def main():
    prompts = [
        "Tell me a joke.",
        "Write a poem about the moon.",
        "Summarize the latest AI advancements."
    ]

    start_time = time.time()
    await process_multiple_tasks(prompts)
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.2f} seconds")

# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())