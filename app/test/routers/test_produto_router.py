from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Produtos as ProdutoModel
from app.main import app

client = TestClient(app)

def test_add_produto_route(db_session, categorias_no_db):
    body = {
        "categoria_slug":categorias_no_db[0].slug,
        "produto":{
            "nome": "Camisa Adidas",
            "slug": "camisa-adidas",
            "preco": 23.99,
            "quantidade": 23
        }
    }
    
    response = client.post('/produtos/add', json=body)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    produtos_no_db = db_session.query(ProdutoModel).all()
    
    assert len(produtos_no_db) == 1
    
    db_session.delete(produtos_no_db[0])
    db_session.commit()

    
def test_add_produto_route_categoria_slug_invalida(db_session):
    body = {
        "categoria_slug": 'Categoria Invalida',
        "produto":{
            "nome": "Camisa Adidas",
            "slug": "camisa-adidas",
            "preco": 23.99,
            "quantidade": 23
        }
    }
    
    response = client.post('/produtos/add', json=body)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    produtos_no_db = db_session.query(ProdutoModel).all()
    
    assert len(produtos_no_db) == 0
    

def test_update_produto_route(db_session, produto_no_db):
    body = {
        "nome": "Atualizar Camisa",
        "slug": "atualizar-camisa",
        "preco": 23.88,
        "quantidade": 10
    }
    
    response = client.put(f'/produtos/update/{produto_no_db.id}', json=body)
    
    assert response.status_code == status.HTTP_200_OK
    
    db_session.refresh(produto_no_db)
    
    produto_no_db.nome == "Atualizar Camisa"
    produto_no_db.slug == "atualizar-camisa"
    produto_no_db.preco == 23.88    
    produto_no_db.quantidade == 10    
    
    
def test_update_produto_route_invalid_id():
    body = {
        "nome": "Atualizar Camisa",
        "slug": "atualizar-camisa",
        "preco": 23.88,
        "quantidade": 10
    }
    
    response = client.put(f'/produtos/update/1', json=body)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_produto_route(db_session, produto_no_db):
    response = client.delete(f'/produtos/delete/{produto_no_db.id}')
    
    assert response.status_code == status.HTTP_200_OK
    
    produto_no_db = db_session.query(ProdutoModel).all()
    
    assert len(produto_no_db) == 0
    
def test_delete_produto_route_invalid_id():
    response = client.delete(f'produtos/delete/1')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND