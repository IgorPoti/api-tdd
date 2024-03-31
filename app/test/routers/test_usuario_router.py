from fastapi.testclient import TestClient
from fastapi import status
from app.schemas.usuario import Usuario
from app.db.models import Usuario as UsuarioModel
from app.main import app

client = TestClient(app)

def test_registro_usuario_route(db_session):
    body = {
        'nome':'Joao',
        'senha': 'admin#'
    }
    
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    
    response = client.post('/usuario/registrar', json=body, headers=headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    usuario_no_db = db_session.query(UsuarioModel).first()
    assert usuario_no_db is not None
    
    db_session.delete(usuario_no_db)
    db_session.commit()

def test_registro_usuario_route_ja_existe(usuario_no_db):
    body = {
        'nome': usuario_no_db.nome,
        'senha': 'admin#'
    }
    
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
        }

    response = client.post('/usuario/registrar', json=body, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    

def test_usuario_login_route(usuario_no_db):
    body = {
        'username': usuario_no_db.nome,
        'password': 'admin#'
    }
    
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    
    response = client.post('/usuario/login', data=body, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'acess_token' in data
    assert 'expires_at' in data
    
    
def test_usuario_login_route_usuario_invalido(usuario_no_db):
    body = {
        'username': 'Invalido',
        'password': 'admin#'
    }
    
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    
    response = client.post('/usuario/login', data=body, headers=headers)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_usuario_login_route_senha_invalido(usuario_no_db):
    body = {
        'username': usuario_no_db.nome,
        'password': 'Invalido'
    }
    
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    
    response = client.post('/usuario/login', data=body, headers=headers)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    