from fastapi import FastAPI
from models import Base
from database import engine
from routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)  # Creates tables

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Hello Event Registration System"}
