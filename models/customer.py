from beanie import Document
from pydantic import EmailStr
from typing import Optional

class Customer(Document):
    id: int
    firstName: str
    lastName: str
    phone: str
    email: Optional[EmailStr]

    class Settings:
        name = "customer"