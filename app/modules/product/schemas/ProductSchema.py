from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name:str
    price:float
    #category_id:int

class ProductSchema(ProductBase):
    id:int 
    created_at:datetime
    
    class Config:
        orm_mode=True
