from decimal import Decimal

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category: str
    price: Decimal


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
