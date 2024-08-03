# src/db/models/document.py

from typing import List, Optional
from pydantic import Field
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId with value: {v} from cls {cls}")
            
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")

class Document(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    embedding:Optional[List[float]] = []
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

