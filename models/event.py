from beanie import Document

class Event(Document):
    clientId: str
    name: str
    quantityPictureChoose: int
    totalPictures: int
    pathToFolder: str

    class Settings:
        name = "event"