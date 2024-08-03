from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId

from .document import PyObjectId

class Users(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    password: str
    income:Optional[str] 
    expenses: Optional[str]
    debt:Optional[str] 
    generated: Optional[str] = None
    full_name: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}