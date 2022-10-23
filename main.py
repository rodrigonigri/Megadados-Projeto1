# Importando bibliotecas necessárias

from matplotlib.pyplot import title
from sqlalchemy import desc
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Body
from fastapi import Query
from fastapi import status
from fastapi.responses import HTMLResponse

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

# Inicio
@app.get("/", status_code = status.HTTP_200_OK)
async def root():
    """
    Apenas uma home page com gosto de macarrão
    """
    content = """
<body>
    <li> <a href="http://127.0.0.1:8000/itens">Para acessar a lista de produtos</a> </li>

    <li> <a href="http://127.0.0.1:8000/itens/0">Para acessar um produto com id específico</a> </li>

    <li> <a href="http://127.0.0.1:8000/docs">Para ver utilizar o CRUD</a> </li>

</body>
    """
    return HTMLResponse(content=content)

# get all
@app.get("/itens")
async def get_produtos():
    return produtos

# get by id
@app.get("/itens/{id}")
async def get_produto(id: int):
    for produto in produtos:
        if produto.id == id:
            return produto
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Produto não encontrado")

# --------------------------- POST ---------------------------

@app.post("/itens/", status_code = status.HTTP_201_CREATED)
async def post_produto(produto: Produto = Body(
        title="Add produto",
        description="Produto a ser adicionado via Body",
        example={
            "id": 3,
            "name": "banana"
        })):
    produtos.append(produto)
    return produto

# --------------------------- PUT ---------------------------

@app.put("/itens/{id}", status_code = status.HTTP_202_ACCEPTED)
async def put_produto(produto: Produto = Body(
        title="Update Produto",
        description="Atualizar produto via Body",
        example={
            "id": 3,
            "name": "banana"
        })):
    for prod in produtos:
        if prod.id == produto.id: 
            prod.name = produto.name 
            return prod
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

# --------------------------- DELETE ---------------------------

@app.delete("/itens/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_produto(id: int = Path(
    title="Delete produto",
    description="Deletar produto pelo id",
    )):
    for produto in produtos:
        if produto.id == id:
            produtos.remove(produto)
            return "Produto removido com sucesso"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")