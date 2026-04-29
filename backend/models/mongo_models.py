from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# Custom type for handling MongoDB ObjectIds in Pydantic models
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    author_id: int  # This links to the PostgreSQL User.id
    title: str
    content: str
    tags: List[str] = []
    likes: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Comment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    post_id: PyObjectId # Reference to the Post MongoDB document
    author_id: int # Links to PostgreSQL User.id
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
