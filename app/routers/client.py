from fastapi import   status,HTTPException,Depends,APIRouter,Response
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from ..database import  engine,get_db

router=APIRouter(
    prefix="/client",
    tags=["Client"]
)

@router.put("/purshase")
async def purshase(product:schemas.ProductBase,quantity:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    remaining_products=db.query(models.Product).count()

    if remaining_products<quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You requested more than the remaining quantity, we have "+remaining_products+" products.")

    totale_price=product.price*quantity
    if current_user.balance<totale_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your balance is not enough to buy what you requested.")

    client_query= db.query(models.Post).filter(models.Post.id == id)
    client_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/{id}',response_model=schemas.UserOut)
def get_client(id:int,db: Session = Depends(get_db)):
    print(id)
    user = db.query(models.User).filter(models.User.id == id ).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user

