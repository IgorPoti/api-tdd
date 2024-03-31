import pytest
from datetime import datetime, timedelta
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
    

def test_usuario_login(db_session, usuario_no_db):
    uc = UsuarioUseCases(db_session=db_session)
   
    usuario = Usuario(
        nome=usuario_no_db.nome,
        senha='admin#'
    )
    
    token_data = uc.usuario_login(usuario=usuario, expires_in=30)
    
    assert token_data.expires_at < datetime.now() + timedelta(31)
    

def test_usuario_login_nome_invalido(db_session):
    uc = UsuarioUseCases(db_session=db_session)
   
    usuario = Usuario(
        nome='teste',
        senha='admin#'
    )
    
    with pytest.raises(HTTPException):
        uc.usuario_login(usuario=usuario, expires_in=30)
        

def test_usuario_login_senha_invalida(db_session, usuario_no_db):
    uc = UsuarioUseCases(db_session=db_session)
   
    usuario = Usuario(
        nome=usuario_no_db.nome,
        senha='admis'
    )
    
    with pytest.raises(HTTPException):
        uc.usuario_login(usuario=usuario, expires_in=30)