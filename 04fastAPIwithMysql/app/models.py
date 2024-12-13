from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)  # Specify length for VARCHAR
    description = Column(String(500), index=True)  # Specify length for VARCHAR
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)