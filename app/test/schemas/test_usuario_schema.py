import pytest
from app.schemas.usuario import Usuario

def test_usuario_schema():
    usuario = Usuario(nome='Joao', senha='123')
    
    assert usuario.dict() == {
        'nome': 'Joao',
        'senha': '123'
    }
    
def test_usuario_schema_usuario_invalido():
    with pytest.raises(ValueError):
        usuario = Usuario(nome='João#', senha='123#')
    
    