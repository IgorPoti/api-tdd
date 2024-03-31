import pytest
from datetime import datetime
from app.schemas.usuario import Usuario, TokenData

def test_usuario_schema():
    usuario = Usuario(nome='Joao', senha='123')
    
    assert usuario.dict() == {
        'nome': 'Joao',
        'senha': '123'
    }
    
def test_usuario_schema_usuario_invalido():
    with pytest.raises(ValueError):
        usuario = Usuario(nome='João#', senha='123#')
    

def test_token_data():
    expires_at = datetime.now()
    token_data = TokenData(
        acess_token='token qualquer',
        expires_at = expires_at
    )
    
    assert token_data.dict() == {
        'acess_token': 'token qualquer',
        'expires_at': expires_at
    }