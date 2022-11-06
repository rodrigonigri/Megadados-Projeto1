# Importando bibliotecas necessárias
from matplotlib.pyplot import title
from sqlalchemy import desc
from fastapi import Depends, FastAPI, HTTPException, Path, Body, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Union, Optional, List
from pydantic import BaseModel

# Importando arquivos do projeto
from . import models, schemas, crud
from .database import SessionLocal, engine

# Criando as tabelas da base de dados:
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------- GET ---------------------------

# Inicio
@app.get("/", status_code = status.HTTP_200_OK)
async def root():
    """
    Apenas uma home page com gosto de macarrão
    """
    content = """
<body>
    <li> <a href="http://127.0.0.1:8000/itens">Para acessar a lista de produtos</a> </li>

    <li> <a href="http://127.0.0.1:8000/itens/1">Para acessar um produto com id específico</a> </li>

    <li> <a href="http://127.0.0.1:8000/docs">Para ver utilizar o CRUD</a> </li>

</body>
    """
    return HTMLResponse(content=content)

# get all
@app.get("/itens")
def get_produtos(db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return products

# get by id
@app.get("/itens/{id}")
def get_produto(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=id)
    if db_product is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Produto não encontrado")
    return db_product

# --------------------------- POST ---------------------------

@app.post("/itens/", status_code = status.HTTP_201_CREATED)
def post_produto(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto já existente no inventário")
    return crud.create_product(db=db, product=product)

@app.post("/itens/{quantity}", status_code = status.HTTP_201_CREATED)
def post_transacao(quantity: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        crud.create_transaction(db=db, transaction=transaction, quantity=quantity)
        return "Produto adicionado ao inventário com sucesso"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não existente no inventário")

# --------------------------- PUT ---------------------------

@app.put("/itens/{id}", status_code = status.HTTP_201_CREATED)
def put_produto(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        crud.update_product(db=db, product_id=id, product=product)
        return "Produto atualizado com sucesso"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não existente no inventário")

# -------------------------- DELETE ---------------------------

@app.delete("/itens/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_produto(id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_product(db, product_id=id)
        return "Produto removido com sucesso"
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")