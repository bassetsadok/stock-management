from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None