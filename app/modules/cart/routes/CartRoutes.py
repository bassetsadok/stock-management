from typing import List
from app.modules.cart.schemas.CartSchema import cart_base, cart_item_base, cart_item_schema, cart_schema
from app.modules.product.models.Product import Product

from app.modules.product.schemas.ProductSchema import ProductBase, ProductSchema
from ....autherization import oauth2
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....db.database import  engine,get_db
from ...category.models.Category import Category
from ...cart.models.Cart import Cart,CartItem
from ...inventory.models.Inventory import Inventory
router=APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=cart_item_schema)
async def add_to_cart(cart_item:cart_item_base,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action.")
    
    print(cart_item)
    print("1")

    product_avalaibility_check = db.query(Inventory).filter(Inventory.product_id == cart_item.product_id ).first()
    if not product_avalaibility_check.quantity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This product is not available.")
    print("2")

    print("iam here")
    cart_query = db.query(Cart).filter(Cart.user_id == current_user.id )
    cart=cart_query.first()
    product = db.query(Product).filter(Product.id == cart_item.product_id ).first()
    print("3")

    price=cart_item.quantity*product.price

    print("4")
    print("heyyyyy",cart)

    new_cart_item=CartItem(cart_id=cart.id,price=price,**cart_item.dict())
    print("5")
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    cart.total_price=cart.total_price+price

    # cart_query.update(cart,synchronize_session=False)
    # db.commit()
    updated_cart=cart_schema(id=cart.id,user_id=cart.user_id,total_price=cart.total_price+price)
    cart_query.update(updated_cart.dict(),synchronize_session=False)
    db.commit()
    print("6")

    return new_cart_item


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