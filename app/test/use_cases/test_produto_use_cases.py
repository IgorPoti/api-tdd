import pytest
from fastapi import HTTPException
from app.db.models import Produtos as ProdutoModel
from app.schemas.produto import Produto, ProdutoOutput
from app.use_cases.produto import ProdutoUseCases


def test_add_produto_uc(db_session, categorias_no_db):
    uc = ProdutoUseCases(db_session)
    
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=22.99,
        quantidade=22
    )
    
    uc.add_produto(produto=produto, categoria_slug=categorias_no_db[0].slug)
    
    produto_no_db = db_session.query(ProdutoModel).first()
    
    assert produto_no_db is not None
    assert produto_no_db.nome == produto.nome
    assert produto_no_db.slug == produto.slug
    assert produto_no_db.preco == produto.preco
    assert produto_no_db.quantidade == produto.quantidade
    assert produto_no_db.categoria.nome == categorias_no_db[0].nome
    
    db_session.delete(produto_no_db)
    db_session.commit()

def test_produto_uc_categoria_invalida(db_session):
    uc = ProdutoUseCases(db_session)
    
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=22.99,
        quantidade=22
    )
    with pytest.raises(HTTPException):
     uc.add_produto(produto=produto, categoria_slug='Categoria Invalida')
     
def test_update_produto(db_session, produto_no_db):
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=22.99,
        quantidade=22
    )   
    
    uc = ProdutoUseCases(db_session=db_session)
    
    uc.update_produto(id=produto_no_db.id, produto=produto)
    
    produto_update_no_db = db_session.query(ProdutoModel).filter_by(id=produto_no_db.id).first()
    
    assert produto_update_no_db is not None
    assert produto_update_no_db.nome == produto.nome
    assert produto_update_no_db.slug == produto.slug
    assert produto_update_no_db.preco == produto.preco
    assert produto_update_no_db.quantidade == produto.quantidade

def test_update_produto_invalid_id(db_session):
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=22.99,
        quantidade=22
    )   
    
    uc = ProdutoUseCases(db_session=db_session)
    
    with pytest.raises(HTTPException):
        uc.update_produto(id=1, produto=produto)
        
def test_delete_produto(db_session, produto_no_db):
        uc = ProdutoUseCases(db_session=db_session)
        uc.delete_produto(id=produto_no_db.id)
        
        produto_no_db = db_session.query(ProdutoModel).all()
        
        assert len(produto_no_db) == 0
        
def test_delete_produto_nao_existe(db_session):
        uc = ProdutoUseCases(db_session=db_session)
        
        with pytest.raises(HTTPException):
            uc.delete_produto(id=1)


def test_list_produtos(db_session, produtos_no_db):
    uc = ProdutoUseCases(db_session=db_session)
    
    produtos = uc.list_produtos()
    
    for produto in produtos_no_db:
        db_session.refresh(produto)
    
    assert len(produtos) == 4
    assert type(produtos[0]) == ProdutoOutput
    assert produtos[0].nome == produtos_no_db[0].nome
    assert produtos[0].categoria.nome == produtos_no_db[0].categoria.nome
    
    
def test_list_produtos_com_search(db_session, produtos_no_db):
    uc = ProdutoUseCases(db_session=db_session)
    
    produtos = uc.list_produtos(search='adidas')
    
    for produto in produtos_no_db:
        db_session.refresh(produto)
    
    assert len(produtos) == 3
    assert type(produtos[0]) == ProdutoOutput
    assert produtos[0].nome == produtos_no_db[0].nome
    assert produtos[0].categoria.nome == produtos_no_db[0].categoria.nome