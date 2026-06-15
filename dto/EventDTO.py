from pydantic import BaseModel

class EventDTO(BaseModel):
    client_Id: int
    name: str
    QuantityPictureChoose: int
    totalPictures: int
    pathToFolder: str