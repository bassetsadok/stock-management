from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship
from ....db.database import Base

class Category(Base):
    __tablename__ = "categories"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    #product = relationship("Product", back_populates="category")
