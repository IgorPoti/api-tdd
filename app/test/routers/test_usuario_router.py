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
    
    response = client.post('/usuario/registrar', json=body)
    
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

    response = client.post('/usuario/registrar', json=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    