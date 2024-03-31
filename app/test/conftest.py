import pytest
from passlib.context import CryptContext
from app.db.connection import Session
from app.db.models import Categoria as CategoriaModel
from app.db.models import Produtos as ProdutoModel
from app.db.models import Usuario as UsuarioModel

crypt_context = CryptContext(schemes=['sha256_crypt'])

@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()
        
@pytest.fixture()
def categorias_no_db(db_session):
    categorias = [
        CategoriaModel(nome='Roupa', slug='roupa'),
        CategoriaModel(nome='Carro', slug='carro'),
        CategoriaModel(nome='Itens de cozinha', slug='itens-de-cozinha'),
        CategoriaModel(nome='Decoracao', slug='decoracao'),
    ]
    
    for categoria in categorias:
        db_session.add(categoria)
    db_session.commit()
    
    for categoria in categorias:
        db_session.refresh(categoria)
        
    yield categorias

    for categoria in categorias:
        db_session.delete(categoria)
    db_session.commit()

@pytest.fixture()
def produto_no_db(db_session):
    categoria = CategoriaModel(nome='Roupa', slug='roupa')
    db_session.add(categoria)
    db_session.commit()
    
    produto = ProdutoModel(
        nome = 'Camisa Adidas',
        slug = 'camisa-adidas',
        preco = 109.99,
        quantidade = 20,
        categoria_id = categoria.id
        
    )
    
    db_session.add(produto)
    db_session.commit()
    
    yield produto
    
    db_session.delete(produto)
    db_session.delete(categoria)
    db_session.commit()
    
@pytest.fixture()
def produtos_no_db(db_session):
    categoria = CategoriaModel(nome='Roupa', slug='roupa')
    
    db_session.add(categoria)
    db_session.commit()
    db_session.refresh(categoria)
    
    produtos = [
        ProdutoModel(nome='Camisa Adidas', slug='camisa-adidas', preco=100, quantidade=10, categoria_id=categoria.id),
        ProdutoModel(nome='Short Adidas', slug='short', preco=100, quantidade=10, categoria_id=categoria.id),
        ProdutoModel(nome='Moletom', slug='moletom-adidas', preco=100, quantidade=10, categoria_id=categoria.id),
        ProdutoModel(nome='Camisa', slug='camisa', preco=100, quantidade=10, categoria_id=categoria.id)
    ]
    
    for produto in produtos:
        db_session.add(produto)
    db_session.commit()
    
    for produto in produtos:
        db_session.refresh(produto)
        
    yield produtos

    for produto in produtos:
        db_session.delete(produto)
    db_session.delete(categoria)
    db_session.commit()
    
    
@pytest.fixture()
def usuario_no_db(db_session):
    usuario = UsuarioModel(
        nome='Joao',
        senha=crypt_context.hash('admin#')
    )
    
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    
    yield usuario
    
    db_session.delete(usuario)
    db_session.commit()