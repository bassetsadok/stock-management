from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    name=Column(String,nullable=False)
    admin=Column(Boolean)
    balance=Column(Float,nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Category(Base):
    __tablename__ = "categories"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    product = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    price=Column(Float,nullable=True)
    category_id=Column(Integer,ForeignKey("categories.id",ondelete="CASCADE"),nullable=False)
    category = relationship("Category", back_populates="product")
