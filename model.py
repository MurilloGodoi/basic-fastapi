from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    category = Column(String)
    price = Column(Numeric(2))
