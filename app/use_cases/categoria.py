from sqlalchemy.orm import Session
from app.db.models import Categoria as CategoriaModel
from app.schemas.categoria import Categoria, CategoriaOutPut
from fastapi import HTTPException, status


class CategoriaUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add_categoria(self, categoria: Categoria):
        categoria_model = CategoriaModel(**categoria.dict())
        self.db_session.add(categoria_model)
        self.db_session.commit()
        
        
    def list_categorias(self):
        categorias_no_db = self.db_session.query(CategoriaModel).all()
        categorias_output = [
            self.serialize_categoria(categoria_model)
            for categoria_model in categorias_no_db
        ]
        
        return categorias_output
    
    
    def delete_categoria(self, id:int):
        categoria_model = self.db_session.query(CategoriaModel).filter_by(id=id).first()
        if not categoria_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não localizada')
        self.db_session.delete(categoria_model)
        self.db_session.commit()
        
        
    def serialize_categoria(self, categoria_model: CategoriaModel):
        return CategoriaOutPut(**categoria_model.__dict__)
        