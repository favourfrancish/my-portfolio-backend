from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

db = client["portfolio"]
contacts_collection = db["contacts"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Contact(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
def index():
    return {"Message": "Portfolio API is working"}


@app.post("/contact")
def contact(message: Contact):
    contacts_collection.insert_one(message.model_dump())

    return {"Message Sent": message}
