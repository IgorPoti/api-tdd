from decouple import config
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.schemas.usuario import Usuario, TokenData
from app.db.models import Usuario as UsuarioModel

crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

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
        except IntegrityError:
            self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario já cadastrado! Tente com outro nome.')
        
    def usuario_login(self, usuario: Usuario, expires_in: int = 30):
        usuario_no_db = self._get_usuario(nome=usuario.nome)
        
        if usuario_no_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário ou senha não é valido')
        
        if not crypt_context.verify(usuario.senha, usuario_no_db.senha):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário ou senha não é valido')
        
        expires_at = datetime.now() + timedelta(expires_in)
        
        data = {
            'sub': usuario_no_db.nome,
            'exp': expires_at
        }
        
        acess_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        token_data = TokenData(acess_token=acess_token, expires_at=expires_at)
        
        return token_data
    
    def verificar_token(self, token:str):
        try:
            data = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido!')
        
        usuario_no_db = self._get_usuario(nome=data['sub'])
        
        if usuario_no_db is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido!')
            
    
    def _get_usuario(self, nome: str, ):
        usuario_no_db = self.db_session.query(UsuarioModel).filter_by(nome=nome).first()
        return usuario_no_db
        