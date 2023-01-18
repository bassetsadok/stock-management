from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Float)
    user = relationship("User", back_populates="cart")
    cart_item = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    cart = relationship("Cart", back_populates="cart_item")
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="cart_item")
    quantity = Column(Integer)
    price = Column(Float)
