from typing import List
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import  engine,get_db

router=APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Product)
async def create_product(product:schemas.ProductBase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")
    
    print(product.category_id)


    category = db.query(models.Category).filter(models.Category.id == product.category_id ).first()

    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not exist")

    print("iam here")
    new_product=models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/",response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    products=db.query(models.Product).all()
    return products

@router.get('/{id}',response_model=schemas.Product)
def get_product(id:int,db: Session = Depends(get_db)):
    print(id)
    product = db.query(models.Product).filter(models.Product.id == id ).first()
    print(product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
    
    return product