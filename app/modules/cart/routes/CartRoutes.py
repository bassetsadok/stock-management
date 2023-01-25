from typing import List
from app.modules.cart.schemas.CartSchema import cart_base, cart_item_base, cart_item_schema, cart_schema
from app.modules.product.models.Product import Product

from app.modules.product.schemas.ProductSchema import  ProductSchema
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

#User add item to his card
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=cart_item_schema)
async def add_to_cart(cart_item:cart_item_base,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action.")
    #check if product available in inventory
    product_avalaibility_check = db.query(Inventory).filter(Inventory.product_id == cart_item.product_id ).first()
    if product_avalaibility_check.quantity <cart_item.quantity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This product is not available.")
    cart_query = db.query(Cart).filter(Cart.user_id == current_user.id )
    cart=cart_query.first()
    product = db.query(Product).filter(Product.id == cart_item.product_id ).first()
    #check if user is already checked this product before
    cart_item_for_same_prod_query=db.query(CartItem).filter(CartItem.product_id==cart_item.product_id)
    cart_item_for_same_prod=cart_item_for_same_prod_query.first()
    #update the totale price in the cart
    price=cart_item.quantity*product.price
    cart.total_price=cart.total_price+price
    updated_cart=cart_schema(id=cart.id,user_id=cart.user_id,total_price=cart.total_price+price)
    cart_query.update(updated_cart.dict(),synchronize_session=False)
    db.commit()
    #if user already choose product and want to add more we dont need to create a new cart item, we will add on this
    if cart_item_for_same_prod != None :
        quantity=cart_item_for_same_prod.quantity+cart_item.quantity
        price=cart_item_for_same_prod.price+(cart_item.quantity*product.price)
        cart_item_for_same_prod_scoop=cart_item_schema(id=cart_item_for_same_prod.id,cart_id=cart.id,product_id=product.id,quantity=quantity,price=price)
        cart_item_for_same_prod_query.update(cart_item_for_same_prod_scoop.dict(),synchronize_session=False)
        db.commit()
        db.refresh(cart_item_for_same_prod)
        return cart_item_for_same_prod
    #when choosing product for the first time we create a new cart item
    else:     
        new_cart_item=CartItem(cart_id=cart.id,price=price,**cart_item.dict())
        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)
        return new_cart_item

#Get all user's cart items
@router.get("/items",response_model=List[cart_item_schema])
async def get_products(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()
    cart_items=db.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    return cart_items

#Get one user's cart item
@router.get('/items/{id}',response_model=cart_item_schema)
def get_product(id:int,db: Session = Depends(get_db)):
    cart_item=db.query(CartItem).filter(CartItem.id==id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"cart item with id: {id} does not exist")
    
    return cart_item

#Delete cart item from the cart
@router.delete("/items/{id}")
async def delete_cart_item(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    cart_item_query=db.query(CartItem).filter(CartItem.id==id)
    cart_item=cart_item_query.first()

    if cart_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cart item {id} was not found")
    
    cart_item_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
