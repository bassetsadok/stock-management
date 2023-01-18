from app.modules.user.schemas.UserSchema import UserCreate, UserOut
from ....utilities import utils
from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from ....db import  database
from ....autherization.auth import oauth2
from ...user.models.User import User
from ...product.schemas.ProductSchema import ProductBase
from ...product.models.Product import Product
from ...cart.models.Cart import Cart
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db: Session = Depends(database.get_db)):


    #hash the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_cart=Cart(user_id=new_user.id,total_price=0)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return new_user

@router.put("/purshase")
async def purshase(product:ProductBase,quantity:int,db: Session = Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):

    remaining_products=db.query(Product).count()

    if remaining_products<quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You requested more than the remaining quantity, we have "+remaining_products+" products.")


    client_query= db.query(User).filter(User.id == id)
    client_query.update(product.dict(),synchronize_session=False)
    db.commit()

    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/{id}',response_model=UserOut)
def get_client(id:int,db: Session = Depends(database.get_db)):
    print(id)
    user = db.query(User).filter(User.id == id ).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user

