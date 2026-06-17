from pydantic import BaseModel


class CustomerLoginRequest(BaseModel):
    firstName: str
    lastName: str
    password: str