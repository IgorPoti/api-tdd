import pytest
from app.schemas.produto import Produto, ProdutoInput, ProdutoOutput
from app.schemas.categoria import Categoria

def test_produto_schema():
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=25.99,
        quantidade=25
    )
    
    assert produto.dict() =={
        'nome':'Camisa Adidas',
        'slug':'camisa-adidas',
        'preco':25.99,
        'quantidade':25
    }
    
    
def test_produto_schema_invalid_slug():
    with pytest.raises(ValueError):
        produto = Produto(
            nome='Camisa Adiddas',
            slug='camisa adiddas',
            preco=25.99,
            quantidade=25
        )
        
    with pytest.raises(ValueError):
        produto = Produto(
            nome='Camisa Adiddas',
            slug='níke',
            preco=25.99,
            quantidade=25
        )
        
    with pytest.raises(ValueError):
        produto = Produto(
            nome='Camisa Adidas',
            slug='Camisa-adidas',
            preco=25.99,
            quantidade=25
        )

def test_produto_schema_invalid_price():
    with pytest.raises(ValueError):
        produto = Produto(
            nome='Camisa Adidas',
            slug='Camisa-adidas',
            preco=0,
            quantidade=25
        )    
        

def test_produto_input_schema():
    produto = Produto(
        nome='Camisa Adidas',
        slug='camisa-adidas',
        preco=25.99,
        quantidade=25
    )    
    
    produto_input = ProdutoInput(
        categoria_slug = 'roupa',
        produto=produto
        
        )
    
    assert produto_input.dict() == {
        'categoria_slug': 'roupa',
        'produto':{
            'nome': 'Camisa Adidas',
            'slug': 'camisa-adidas',
            'preco': 25.99,
            'quantidade': 25
        }
    }
    
    
 
def test_produto_output_schema():
        categoria = Categoria(
            nome='Roupa',
            slug='roupa'
        )
        produto_output = ProdutoOutput(
            id=1,
            nome='Camisa Adidas',
            slug='camisa-adidas',
            preco= 10,
            quantidade=10,
            categoria=categoria
        )
        
        assert produto_output.dict() == {
            "id":1,
            "nome": "Camisa Adidas",
            "slug": "camisa-adidas",
            "preco": 10,
            "quantidade":10,
            "categoria": {
                'nome':'Roupa',
                'slug': 'roupa'
            }
        }