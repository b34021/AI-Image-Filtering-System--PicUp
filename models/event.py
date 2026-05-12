from beanie import Document

class Event(Document):
    id: int
    clientId: int
    name: str
    QuentityPictureChoose: int
    totalPictures: int
    pathToFolder: str

    class Settings:
        name = "event"