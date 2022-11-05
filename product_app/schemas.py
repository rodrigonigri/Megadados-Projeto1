from typing import List, Union
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    quantity: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    name: str
    quantity: int

class TransactionCreate(ProductBase):
    pass

class Transaction(ProductBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True