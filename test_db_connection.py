from pymongo import MongoClient
from  services.config import MONGO_URI
client = MongoClient(MONGO_URI)  # או כתובת השרת שלך

try:
    # הפקודה ping בודקת שהחיבור פעיל
    client.admin.command("ping")
    print("החיבור הצליח!")
except Exception as e:
    print("החיבור נכשל:", e)

db = client["pic_up"]  # החלף בשם בסיס הנתונים שלך
collection = db["category"]  # החלף בשם הקולקציה שלך

# מנסה למצוא מסמך ראשון
doc = collection.find_one()
print(doc)
result = collection.insert_one({"test": "value"})
print("מספר מזהה:", result.inserted_id)


# None אם אין מסמכים, אחרת מציג את המסמך