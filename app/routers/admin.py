from fastapi import   status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import  engine,get_db

router=APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get('/{id}',response_model=schemas.UserOut)
def get_admin(id:int,db: Session = Depends(get_db)):
    print(id)
    user = db.query(models.User).filter(models.User.id == id ).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user