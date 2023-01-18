from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    name:str
    admin:bool
    
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

