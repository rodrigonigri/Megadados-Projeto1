# Importando bibliotecas necessárias

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Body
from fastapi import Query
from fastapi import status

from typing import Union
from typing import Optional

from pydantic import BaseModel

# Criando classe Produto 

class Produto(BaseModel):
    id: int
    name: str

# Criando produtos

shampoo = Produto(id = 0, name = "Shampoo")
sorvete = Produto(id = 1, name = "Sorvete")

produtos = [shampoo, sorvete]

# Criando CRUD

app = FastAPI()

# --------------------------- GET ---------------------------

@app.get("/")
async def root():
    return "Digite '/itens' para GET e POST , ou '/itens/{id}' para GET, PUT, PATCH e DELETE"

@app.get("/itens")
async def get_produtos():
    return produtos

@app.get("/itens/{id}")
async def get_produto(id: int):
    for produto in produtos:
        if produto.id == id:
            return produto
    return "Incorrect ID"

# --------------------------- POST ---------------------------

@app.post("/itens/")
async def post_produto(produto: Produto = Body(
        example={
            "id": 3,
            "name": "banana"
        })):
    produtos.append(produto)
    return produto