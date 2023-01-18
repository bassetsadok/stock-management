from app.modules.user.schemas.UserSchema import UserOut
from ....utilities import utils
from fastapi import   status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....db.database import  engine,get_db
from ...user.models.User import User

router=APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get('/{id}',response_model=UserOut)
def get_admin(id:int,db: Session = Depends(get_db)):
    print(id)
    user = db.query(User).filter(User.id == id ).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user