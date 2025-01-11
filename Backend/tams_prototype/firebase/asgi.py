from fastapi import FastAPI
from asgi_vercel import VercelASGI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, Vercel!"}

app = VercelASGI(app)