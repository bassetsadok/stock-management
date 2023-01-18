from typing import Optional
from pydantic import BaseModel, EmailStr

class inventory_base(BaseModel):
    product_id:int
    quantity:int
    availability:Optional[str]

    class Config:
        orm_mode=True

class inventory_schema(inventory_base):
    id:int 

