from typing import List
from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from app.routers.deps import get_db_session, auth
from app.use_cases.produto import ProdutoUseCases
from app.schemas.produto import Produto, ProdutoInput, ProdutoOutput


router = APIRouter(prefix='/produtos', tags=['Produtos'], dependencies=[Depends(auth)])

@router.post('/add', status_code=status.HTTP_201_CREATED, description='Adicionar novo produto')
def add_produto(produto_input: ProdutoInput, db_session: Session = Depends(get_db_session)):
    uc = ProdutoUseCases(db_session=db_session)
    uc.add_produto(produto=produto_input.produto, 
                   categoria_slug=produto_input.categoria_slug)
    
    return Response(status_code=status.HTTP_201_CREATED)

@router.put('/update/{id}', description='Atualizar produto por ID')
def update_produto(id:int, produto: Produto, db_session: Session = Depends(get_db_session)):
    uc = ProdutoUseCases(db_session=db_session)
    uc.update_produto(id=id, produto=produto)
    
    return Response(status_code=status.HTTP_200_OK)

@router.delete('/delete/{id}', description='Deletar Produto')
def delete_produto(id:int, db_session: Session = Depends(get_db_session)):
    
    uc = ProdutoUseCases(db_session=db_session)
    uc.delete_produto(id=id)
    
    return Response(status_code=status.HTTP_200_OK)

@router.get('/list', response_model=List[ProdutoOutput])
def list_produto(search: str= '',
                 db_session: Session = Depends(get_db_session)):
    
    uc = ProdutoUseCases(db_session=db_session)
    produtos = uc.list_produtos(search=search)
    
    return produtos