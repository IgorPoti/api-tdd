import pytest
from app.schemas.categoria import Categoria


def test_categoria_schema():
    categoria = Categoria(
        nome='Roupa',
        slug='roupa'
    )
    
    assert categoria.dict() == {
        'nome': 'Roupa',
        'slug': 'roupa'
    }
    
def test_categoria_schema_invalid_slug():
    with pytest.raises(ValueError):
        categoria = Categoria(
            nome='Roupa',
            slug='roupa de cama'
    )
        
    with pytest.raises(ValueError):
        categoria = Categoria(
            nome='Roupa',
            slug='cão'
    )
    
    with pytest.raises(ValueError):
        categoria = Categoria(
            nome='Roupa',
            slug='Roupa'
    )
    
    