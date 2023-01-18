from .autherization import auth
from .modules.cart.routes import CartRoutes
from .modules.category.routes import CategoryRoutes
from .modules.inventory.routes import InventoryRoutes
from .modules.order.routes import OrderRoutes
from .modules.product.routes import ProductRoutes
from .modules.user.routes import UserRoutes
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .db import  database

from .modules.cart.models import Cart
from .modules.category.models import Category
from .modules.inventory.models import Inventory
from .modules.order.models import Order
from .modules.product.models import Product
from .modules.user.models import User



Cart.Base.metadata.create_all(bind=database.engine)
Category.Base.metadata.create_all(bind=database.engine)
Inventory.Base.metadata.create_all(bind=database.engine)
Order.Base.metadata.create_all(bind=database.engine)
Product.Base.metadata.create_all(bind=database.engine)
User.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(host="localhost",database="stockManagementDb",user="postgres",password="basseT_2000",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was successfull ✅")
        break
    except Exception as error:
        print("connection to database was failed")
        print("error was ",error)
        time.sleep(3)

app.include_router(CartRoutes.router)
app.include_router(CategoryRoutes.router)
app.include_router(InventoryRoutes.router)
app.include_router(OrderRoutes.router)
app.include_router(ProductRoutes.router)
app.include_router(UserRoutes.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello Basset"}
