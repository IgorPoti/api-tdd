from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import status
from fastapi.exceptions import HTTPException
from app.schemas.usuario import Usuario
from app.db.models import Usuario as UsuarioModel

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UsuarioUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def registrar_usuario(self, usuario: Usuario):
        usuario_no_db = UsuarioModel(
            nome = usuario.nome,
            senha = crypt_context.hash(usuario.senha)
        )

        self.db_session.add(usuario_no_db)
        try:
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario já cadastrado! Tente com outro nome.')
        