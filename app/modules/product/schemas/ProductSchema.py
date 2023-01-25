from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name:str
    price:float
    category_id:int

class ProductSchema(ProductBase):
    id:int 
    created_at:datetime
    
    class Config:
        orm_mode=True

class update_product_base(BaseModel):
    name:Optional[str]
    price:Optional[float]
    category_id:Optional[int]

    class Config:
        orm_mode=True
