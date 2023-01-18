from typing import List
from app.modules.cart.schemas.CartSchema import cart_item_base, cart_item_schema
from app.modules.inventory.schemas.InventorySchema import inventory_base,inventory_schema
from app.modules.product.models.Product import Product

from app.modules.product.schemas.ProductSchema import ProductBase, ProductSchema
from ....autherization import oauth2
from fastapi import   Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ....db.database import  engine,get_db
from ...category.models.Category import Category
from ...cart.models.Cart import Cart,CartItem
from ...inventory.models.Inventory import Inventory
from ..models.Order import Order,OrderItem
router=APIRouter(
    prefix="/order",
    tags=["Order"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def confirme_order(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action.")

    cart_query = db.query(Cart).filter(Cart.user_id == current_user.id )
    cart=cart_query.first()
    new_order=Order(user_id=current_user.id,total_price=cart.total_price)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    cart_items_query=db.query(CartItem).filter(CartItem.cart_id==cart.id)
    cart_items=cart_items_query.all()

    for cart_item in cart_items:
        new_order_item=OrderItem(order_id=new_order.id,product_id=cart_item.product_id,quantity=cart_item.quantity,price=cart_item.price)
        db.add(new_order_item)
        db.commit()
        db.refresh(new_order_item)
        product_in_inventory_query = db.query(Inventory).filter(Inventory.product_id == new_order_item.product_id )
        product_in_inventory=product_in_inventory_query.first()
        quantity=product_in_inventory.quantity-new_order_item.quantity

        if quantity > 5:
            availablity="available"
        elif quantity < 5 & quantity > 0:
            availablity="run out soon"
        elif quantity == 0:
            availablity="not available"

        product_in_inventory_updated=inventory_base(product_id=product_in_inventory.product_id,quantity=quantity,availability=availablity)
        product_in_inventory_query.update(product_in_inventory_updated.dict(),synchronize_session=False)
        db.commit()


    cart_items_query.delete()
    db.commit()
    

    # cart = db.query(Cart).filter(Cart.user_id == current_user.id ).first()
    # product = db.query(Product).filter(Product.id == cart_item.product_id ).first()

    # price=cart_item.quantity*product.price
    # new_cart_item=CartItem(cart_id=cart.id,price=price,**cart_item.dict())
    # db.add(new_cart_item)
    # db.commit()
    # db.refresh(new_cart_item)

    return {"d":""}
