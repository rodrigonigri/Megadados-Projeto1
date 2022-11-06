from sqlalchemy.orm import Session
from . import models, schemas

# GET FUNCTIONS -----------------------------------------------------------------------------

def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(models.Product).all()

# POST FUNCTIONS -----------------------------------------------------------------------------

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_transaction(db: Session, transaction: schemas.TransactionCreate, quantity: int):
    old_product = db.query(models.Product).filter(models.Product.name == transaction.name).first()
    old_product.quantity += quantity
    db.commit()

# UPDATE FUNCTIONS -----------------------------------------------------------------------------

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    old_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    old_product.name = product.name
    db.commit()

# DELETE FUNCTIONS -----------------------------------------------------------------------------

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(product)
    db.commit()