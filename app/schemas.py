from pydantic import BaseModel

class VerseInDB(BaseModel):
    reference: str
    text: dict
    count: int

    class Config:
        orm_mode = True

class VerseOut(BaseModel):
    reference: str
    text: dict

class TopVerse(BaseModel):
    reference: str
    count: int
