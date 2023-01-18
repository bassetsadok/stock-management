from typing import List
from app.modules.cart.schemas.CartSchema import cart_item_base, cart_item_schema
from app.modules.inventory.schemas.InventorySchema import inventory_schema, inventory_base
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
    prefix="/inventory",
    tags=["Inventory"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def add_to_inventory(prod_to_inventory:inventory_base,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")
    availablity=""

    #category = db.query(Category).filter(Category.id == product.category_id ).first()

    #if category == None:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not exist")

    product_exist_already_query= db.query(Inventory).filter(Inventory.product_id == prod_to_inventory.product_id)
    product_exist_already=product_exist_already_query.first()

    if product_exist_already != None :
        quantity=product_exist_already.quantity+prod_to_inventory.quantity  

        if quantity > 5:
            availablity="available"
        elif quantity < 5 & quantity > 0:
            availablity="run out soon"
        elif quantity == 0:
            availablity="not available"

        product_exist_already_scoop=inventory_base(product_id=product_exist_already.product_id,quantity=quantity,availablity=availablity)
        product_exist_already_query.update(product_exist_already_scoop.dict(),synchronize_session=False)
        db.commit()
        return product_exist_already
    else:
        if prod_to_inventory.quantity > 5:
            availablity="available"
        elif prod_to_inventory.quantity < 5 & prod_to_inventory.quantity > 0:
            availablity="run out soon"
        elif prod_to_inventory.quantity == 0:
            availablity="not available"
        new_prod_to_inventory=Inventory(availability=availablity,product_id=prod_to_inventory.product_id,quantity=prod_to_inventory.quantity)
        db.add(new_prod_to_inventory)
        db.commit()
        db.refresh(new_prod_to_inventory)
        return new_prod_to_inventory

