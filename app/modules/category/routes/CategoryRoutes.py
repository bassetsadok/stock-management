from typing import List
from app.modules.category.models.Category import Category

from ...category.schemas.CategorySchema import CategoryBase, CategorySchema
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....autherization import oauth2
from ....db import  database

router=APIRouter(
    prefix="/category",
    tags=["Category"]

)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CategorySchema)
async def create_category(category:CategoryBase,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_category=Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/",response_model=List[CategorySchema])
async def get_categories(db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):

    categories=db.query(Category).all()
    return categories

@router.get('/{id}',response_model=CategorySchema)
async def get_category(id:int,dbs: Session = Depends(database.get_db)):
    category = dbs.query(Category).filter(Category.id == id ).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id: {id} does not exist")
    
    return category

#Delete category from db
@router.delete("/{id}")
async def delete_category(id:int,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):

    category_query=db.query(Category).filter(Category.id==id)
    category=category_query.first()

    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cart item {id} was not found")
    
    category_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
