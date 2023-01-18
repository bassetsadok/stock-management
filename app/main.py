from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import  engine,get_db
from . import models
from .routers import admin,auth,user,category,products,client

models.Base.metadata.create_all(bind=engine)

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

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(client.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello Basset"}
