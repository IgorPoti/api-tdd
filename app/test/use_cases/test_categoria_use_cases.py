import pytest
from app.use_cases.categoria import CategoriaUseCases
from app.db.models import Categoria as CategoriaModel
from app.schemas.categoria import Categoria, CategoriaOutPut
from fastapi.exceptions import HTTPException


def test_add_category_uc(db_session):
    uc = CategoriaUseCases(db_session)
    
    categoria = Categoria(
        nome='Roupa',
        slug='roupa'
    )
    
    uc.add_categoria(categoria=categoria)
    
    categorias_no_db = db_session.query(CategoriaModel).all()
    assert len(categorias_no_db) == 1
    assert categorias_no_db[0].nome == 'Roupa'
    assert categorias_no_db[0].slug == 'roupa'
    
    db_session.delete(categorias_no_db[0])
    db_session.commit()
    
def test_list_categorias(db_session, categorias_no_db):
    uc = CategoriaUseCases(db_session=db_session)
    
    categorias = uc.list_categorias()
    
    assert len(categorias) == 4
    assert type(categorias[0]) == CategoriaOutPut
    assert categorias[0].id == categorias_no_db[0].id
    assert categorias[0].nome == categorias_no_db[0].nome
    assert categorias[0].slug == categorias_no_db[0].slug

def test_delete_categoria(db_session):
    categoria_model = CategoriaModel(nome='Roupa', slug='roupa')
    db_session.add(categoria_model)
    db_session.commit()
    
    uc = CategoriaUseCases(db_session=db_session)
    uc.delete_categoria(id=categoria_model.id)
    
    categoria_model = db_session.query(CategoriaModel).first()
    assert categoria_model is None
    
    
def test_delete_categoria_nao_existe(db_session):
    uc = CategoriaUseCases(db_session=db_session)
    
    with pytest.raises(HTTPException):
        uc.delete_categoria(id=1)
    