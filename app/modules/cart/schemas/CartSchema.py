from pydantic import BaseModel, EmailStr

class cart_base(BaseModel):
    id :int
    user_id :int
    total_price : float

class cart_schema(cart_base):
    class Config:
        orm_mode=True


class cart_item_base(BaseModel):
    product_id:int
    quantity:int
    #category_id:int

class cart_item_schema(cart_item_base):
    id:int 
    cart_id:int
    price:float

    class Config:
        orm_mode=True
