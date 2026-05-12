
from beanie import Document

class Category(Document):
    name: str
    key: str
    defaultQuentity: int

    class Settings:
        name = "categories"