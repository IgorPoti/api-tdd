import re
from app.schemas.base import CustomBaseModel
from app.schemas.categoria import Categoria
from pydantic import validator

class Produto(CustomBaseModel):
    nome: str
    slug: str
    preco: float
    quantidade: int

    
    @validator('slug')
    def validar_slug(cls, value):
        if not re.match('^([a-z]|-|_)+$', value):
            raise ValueError('Slug invalido')
        return value    
    
    @validator('preco')
    def validar_preco(cls, value):
        if value <= 0:
            raise ValueError('Preco menor ou igual a zero')
        return value
    

class ProdutoInput(CustomBaseModel):
    categoria_slug: str
    produto: Produto
    
class ProdutoOutput(Produto):
    id: int
    categoria: Categoria