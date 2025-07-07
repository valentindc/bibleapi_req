from pydantic import BaseModel
from pydantic import BaseModel
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional
import re


class VerseReference(BaseModel):
    reference: str = Field(..., min_length=3, max_length=50, example="John 3:16")
    
    @field_validator('reference')
    def validate_reference(cls, v):
        # Basic Bible reference pattern (can be expanded)
        if not re.match(r'^[1-9]?[A-Za-z]+\s+\d+:\d+$', v.strip()):
            raise ValueError('Invalid Bible reference format. Example: "John 3:16"')
        return v.strip().title()


class VerseInDB(BaseModel):
    reference: str
    text: dict
    count: int

    class Config:
        orm_mode = True



class VerseOut(BaseModel):
    reference: str
    text: str  # Changed from dict to str
    translation: Optional[str] = None
    
    class Config:
        from_attributes = True

class TopVerse(BaseModel):
    reference: str
    count: int
