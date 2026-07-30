import os

from fastapi import FastAPI
from dotenv import load_dotenv

from database import supabase

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Server running and connected to Supabase"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 3000)),
        reload=True
    )