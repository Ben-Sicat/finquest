from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from .document import PyObjectId

class Interaction(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    query: str
    response: str
    timestamp: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 