import pytest
from passlib.context import CryptContext
from fastapi import HTTPException
from app.schemas.usuario import Usuario
from app.db.models import Usuario as UsuarioModel
from app.use_cases.usuario import UsuarioUseCases


crypt_context = CryptContext(schemes=['sha256_crypt'])

def test_registro_usuario(db_session):
    usuario = Usuario(
        nome='joao',
        senha='admin#'
    )
    
    uc = UsuarioUseCases(db_session)
    uc.registrar_usuario(usuario=usuario)
    
    usuario_no_db = db_session.query(UsuarioModel).first()
    assert usuario_no_db is not None
    assert usuario_no_db.nome == usuario.nome
    assert crypt_context.verify(usuario.senha, usuario_no_db.senha)
    
    db_session.delete(usuario_no_db)
    db_session.commit()

def test_registro_usuario_atual_existe(db_session):
    
    usuario_no_db = UsuarioModel(
        nome='joao',
        senha=crypt_context.hash('admin#')
    )
    
    db_session.add(usuario_no_db)
    db_session.commit()
    
    uc = UsuarioUseCases(db_session)
    
    usuario = Usuario(
        nome='joao',
        senha=crypt_context.hash('admin#')
    )
    
    with pytest.raises(HTTPException):
        uc.registrar_usuario(usuario=usuario)
        
    db_session.delete(usuario_no_db)
    db_session.commit()