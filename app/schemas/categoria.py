import re
from app.schemas.base import CustomBaseModel
from pydantic import validator


class Categoria(CustomBaseModel):
    nome: str
    slug: str
    
    @validator('slug')
    def validar_slug(cls, value):
        if not re.match('^([a-z]|-|_)+$', value):
            raise ValueError('Slug invalido')
        return value
            
class CategoriaOutPut(Categoria):
    id: int
