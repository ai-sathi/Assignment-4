import os
from fastapi import FastAPI
from dotenv import load_dotenv

from routes.auth import router as auth_router
from routes.public import router as public_router
from routes.protected import router as protected_router

load_dotenv()

app = FastAPI(title="Auth Protect API", version="1.0.0")

app.include_router(auth_router)
app.include_router(public_router)
app.include_router(protected_router)

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