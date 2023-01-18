from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
class CategoryBase(BaseModel):
    name:str

class Category(CategoryBase):
    id:int 
    created_at:datetime

    class Config:
        orm_mode=True

class ProductBase(BaseModel):
    name:str
    price:float
    category_id:int

class Product(ProductBase):
    id:int 
    created_at:datetime
    
    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str
    name:str
    admin:bool
    balance:Optional[int]
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config: 
        orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

    class Config: 
        orm_mode=True

class Token(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None