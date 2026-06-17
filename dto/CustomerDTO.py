from pydantic import BaseModel,EmailStr
from typing import Optional


class CustomerDTO(BaseModel):
    firstName: str
    lastName: str
    clientId:str
    password: str
    phone: str
    email: Optional[EmailStr]