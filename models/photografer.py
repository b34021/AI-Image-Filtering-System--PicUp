from beanie import Document
from pydantic import EmailStr
from typing import Optional

class Photografer(Document):
    id: int
    firstName: str
    lastName: str
    phone: str
    email: Optional[EmailStr]

    class Settings:
        name = "photografer"