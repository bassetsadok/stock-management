from ..utilities import utils
from . import oauth2
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import database
from .TokenSchema import Token
from ..modules.user.models.User import User

router= APIRouter(tags=["authentication"])

@router.post('/login',response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):

    user=db.query(User).filter(User.email== user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")

    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"token":access_token,"token_type":"bearer"}
