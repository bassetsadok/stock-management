from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CategoryBase(BaseModel):
    name:str

class CategorySchema(CategoryBase):
    id:int 
    created_at:datetime

    class Config:
        orm_mode=True

