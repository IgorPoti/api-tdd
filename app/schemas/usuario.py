import re
from pydantic import validator
from app.schemas.base import CustomBaseModel

class Usuario(CustomBaseModel):
    nome: str
    senha: str
    
    @validator('nome')
    def validar_usuario(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Usuário Inválido')
        return value