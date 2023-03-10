from typing import List
from app.modules.product.models.Product import Product

from app.modules.product.schemas.ProductSchema import ProductBase, ProductSchema, update_product_base
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
    product = db.query(Product).filter(Product.id == id ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} does not exist")
    
    return product

#Delete product from db
@router.delete("/{id}")
async def delete_product(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    product_query=db.query(Product).filter(Product.id==id)
    product=product_query.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cart item {id} was not found")
    
    product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update product in db
@router.put("/{id}",response_model=ProductSchema)
async def update_product(id:int,updated_product:update_product_base,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    product_query= db.query(Product).filter(Product.id == id)
    product=product_query.first()

    if product== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"product {id} was not found")
    
    if current_user.admin != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not autherized to perform requested action")
    product_dict=product.__dict__
    updated_product_scoop=ProductSchema(product_dict)
    product_query.update(**updated_product.dict(),synchronize_session=False)
    db.commit()

    return product_query.first()
