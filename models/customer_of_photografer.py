from beanie import Document

class CustomerOfPhotografer(Document):
    id: int
    photograferId: int
    customerId: int
    eventId: int

    class Settings:
        name = "customerOfPhotografer"