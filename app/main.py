from fastapi import FastAPI
from app.routers import auth
from app.database import Base, engine

app = FastAPI(title="FastAPI User Auth")

# Include routers
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "FastAPI app is running!"}

@app.get("/ping")
async def ping():
    return {"status": "ok"}
