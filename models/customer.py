from beanie import Document
from pydantic import EmailStr
from typing import Optional

class Customer(Document):
    firstName: str
    lastName: str
    clientId: str
    password: str
    phone: str
    email: Optional[EmailStr]

    class Settings:
        name = "customer"