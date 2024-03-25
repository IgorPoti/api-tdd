from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Categoria as CategoriaModel
from app.main import app

client = TestClient(app)

def test_categoria_router(db_session):
    body = {
        "name":"Roupa",
        "slug": "roupa"
    }
    
    response = client.post('/categoria/add', json=body)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    categorias_no_db = db_session.query(CategoriaModel).all()
    assert len(categorias_no_db) == 1
    db_session.delete(categorias_no_db[0])
    db_session.commit()


def test_list_categorias_router(categorias_no_db):
    response = client.get('/categoria/list')
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data) == 4
    assert data[0] =={
        "nome":categorias_no_db[0].nome,
        "slug":categorias_no_db[0].slug,
        "id":categorias_no_db[0].id
    }
    
def test_delete_categoria(db_session):
    categoria_model = CategoriaModel(nome='Roupa', slug='roupa')
    db_session.add(categoria_model)
    db_session.commit()
    
    response = client.delete(f'/categoria/delete/{categoria_model.id}')
    
    assert response.status_code == status.HTTP_200_OK
    
    categoria_model = db_session.query(CategoriaModel).first()
    assert categoria_model is None