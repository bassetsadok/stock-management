from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship
from ....db.database import  Base


class Product(Base):
    __tablename__ = "products"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    price=Column(Float,nullable=True)
    category_id=Column(Integer,ForeignKey("categories.id",ondelete="CASCADE"),nullable=False)
    category = relationship("Category", back_populates="product")
    cart_item = relationship("CartItem", back_populates="product")
    order_item = relationship("OrderItem", back_populates="product")
    inventory = relationship("Inventory", back_populates="product")

