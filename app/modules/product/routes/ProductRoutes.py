from typing import List
from app.modules.product.models.Product import Product

from app.modules.product.schemas.ProductSchema import ProductBase, ProductSchema
from ....autherization import oauth2
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....db.database import  engine,get_db
from ...category.models.Category import Category
router=APIRouter(
    prefix="/product",
    tags=["Product"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=ProductSchema)
async def create_product(product:ProductBase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")
    
    print(product.category_id)


    category = db.query(Category).filter(Category.id == product.category_id ).first()

    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not exist")

    print("iam here")
    new_product=Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/",response_model=List[ProductSchema])
async def get_products(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    products=db.query(Product).all()
    return products

@router.get('/{id}',response_model=ProductSchema)
def get_product(id:int,db: Session = Depends(get_db)):
    print(id)
    product = db.query(Product).filter(Product.id == id ).first()
    print(product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
    
    return product