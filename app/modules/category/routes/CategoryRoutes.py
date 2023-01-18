from typing import List

from ...category.models import Category
from ...category.schemas.CategorySchema import CategoryBase, CategorySchema
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....autherization import oauth2
from ....db import  database

router=APIRouter(
    prefix="/category",
    tags=["Category"]

)

@router.get('/{id}')
def get_cat(id:int):
    return {"hello":"world"}



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CategorySchema)
async def create_category(category:CategoryBase,dbs: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_category=Category.Category(**category.dict())
    dbs.add(new_category)
    dbs.commit()
    dbs.refresh(new_category)

    return new_category


@router.get('/{id}',response_model=CategorySchema)
async def get_category(id:int,dbs: Session = Depends(database.get_db)):
    category = dbs.query(Category).filter(Category.id == id ).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")
    
    return category

