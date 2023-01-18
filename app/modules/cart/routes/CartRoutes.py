from typing import List

from app.modules.category.schemas.CategorySchema import CategoryBase, CategorySchema
from ....autherization import oauth2
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....db import  database
from ...category.models import Category

router=APIRouter(
    prefix="/category",
    tags=["Category"]

)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CategoryBase)
async def create_category(category:CategoryBase,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_category=Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get('/{id}',response_model=CategorySchema)
def get_category(id:int,db: Session = Depends(database.get_db)):
    print(id)
    category = db.query(Category).filter(Category.id == id ).first()
    print(category)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")
    
    return category