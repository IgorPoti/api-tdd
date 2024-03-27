from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.schemas.categoria import Categoria, CategoriaOutPut
from app.routers.deps import get_db_session
from app.use_cases.categoria import CategoriaUseCases


router = APIRouter(prefix="/categoria", tags=['Categoria'])


@router.post('/add', status_code=status.HTTP_201_CREATED, description="Adicionar nova categoria")
def add_categoria(categoria: Categoria, 
                  db_session: Session = Depends(get_db_session)
                  ):
    uc = CategoriaUseCases(db_session=db_session)
    uc.add_categoria(categoria=categoria)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/list', response_model=List[CategoriaOutPut], description="List Categorias")
def list_categorias(db_session: Session = Depends(get_db_session)):
    uc = CategoriaUseCases(db_session=db_session)
    response = uc.list_categorias()
    return response

@router.delete('/delete/{id}', description="Deletar Categoria")
def delete_categoria(id: int, db_session: Session = Depends(get_db_session) ):
    
    uc = CategoriaUseCases(db_session=db_session)
    uc.delete_categoria(id=id)
    
    return Response(status_code=status.HTTP_200_OK)