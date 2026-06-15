from pydantic import BaseModel


class BuildRequest(BaseModel):
    path: str
    cust_id: int
    event_id: int