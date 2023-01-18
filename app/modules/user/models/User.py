from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    name=Column(String,nullable=False)
    admin=Column(Boolean)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    cart = relationship("Cart", back_populates="user")
    order = relationship("Order", back_populates="user")

