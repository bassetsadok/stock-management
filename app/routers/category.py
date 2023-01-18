from typing import List
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import  engine,get_db

router=APIRouter(
    prefix="/category",
    tags=["Category"]

)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Category)
async def create_category(category:schemas.CategoryBase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_category=models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get('/{id}',response_model=schemas.Category)
def get_category(id:int,db: Session = Depends(get_db)):
    print(id)
    category = db.query(models.Category).filter(models.Category.id == id ).first()
    print(category)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")
    
    return category