from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
from app.db.models import Produtos as ProdutoModel
from app.db.models import Categoria as CategoriaModel
from app.schemas.produto import Produto, ProdutoOutput


class ProdutoUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def add_produto(self, produto: Produto, categoria_slug: str):
        categoria = self.db_session.query(CategoriaModel).filter_by(slug=categoria_slug).first()
        
        if not categoria:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nenhuma categoria localizada com o slug{categoria_slug}")
        produto_model = ProdutoModel(**produto.dict())
        produto_model.categoria_id = categoria.id
        
        self.db_session.add(produto_model)
        self.db_session.commit()
    
    def update_produto(self, produto: Produto, id: int):
        produto_no_db = self.db_session.query(ProdutoModel).filter_by(id=id).first()
        
        if produto_no_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto localizado com esse ID")
        produto_no_db.nome = produto.nome
        produto_no_db.slug = produto.slug
        produto_no_db.preco = produto.preco
        produto_no_db.quantidade = produto.quantidade
        
        self.db_session.add(produto_no_db)
        self.db_session.commit()
        
    def delete_produto(self, id: int):
        produto_no_db = self.db_session.query(ProdutoModel).filter_by(id=id).first()
        
        if produto_no_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum produto localizado com esse ID")
        
        self.db_session.delete(produto_no_db)
        self.db_session.commit()
        
    def list_produtos(self):
        produtos_no_db = self.db_session.query(ProdutoModel).all()
        
        produtos = [
            self._serialize_produto(produto_no_db)
            for produto_no_db in produtos_no_db
        ]
        
        return produtos
        
    def _serialize_produto(self, produtos_no_db: ProdutoModel):
        produto_dict = produtos_no_db.__dict__
        produto_dict['categoria'] = produtos_no_db.categoria.__dict__
        
        return ProdutoOutput(**produto_dict)