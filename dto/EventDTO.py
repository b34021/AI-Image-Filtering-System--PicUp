from pydantic import BaseModel

class EventDTO(BaseModel):
    clientId: str
    name: str
    quantityPictureChoose: int
    totalPictures: int
    pathToFolder: str