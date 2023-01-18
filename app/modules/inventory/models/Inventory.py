from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="inventory")
    quantity = Column(Integer)
    availability = Column(String)

