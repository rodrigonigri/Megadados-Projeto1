from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Product(Base):
    __tablename__ = "Produtos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    quantity = Column(Integer, default=0)

class Transaction(Base):
    __tablename__ = "Transacao"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)