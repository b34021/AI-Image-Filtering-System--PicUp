from pymongo import MongoClient

uri = "mongodb+srv://miryam_bracha:mb2026@picup.r5cikxn.mongodb.net/?appName=picUp"

client = MongoClient(uri)

db = client["picup_db"]

print("Connected to Atlas")

print("------Connected to cloud--------")

from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)

client.admin.command("ping")

print("Connected")

from pymongo import MongoClient

uri = "mongodb+srv://miryam_bracha:mb2026@picup.r5cikxn.mongodb.net/?appName=picUp"

client = MongoClient(uri)

client.admin.command("ping")

print("OK")