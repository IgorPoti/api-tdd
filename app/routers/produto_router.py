from fastapi import APIRouter, Response, Depends, status
from sqlalchemy.orm import Session
from app.routers.deps import get_db_session
from app.use_cases.produto import ProdutoUseCases
from app.schemas.produto import Produto, ProdutoInput


router = APIRouter(prefix='/produtos')

@router.post('/add')
def add_produto(produto_input: ProdutoInput, db_session: Session = Depends(get_db_session)):
    uc = ProdutoUseCases(db_session=db_session)
    uc.add_produto(produto=produto_input.produto, 
                   categoria_slug=produto_input.categoria_slug)
    
    return Response(status_code=status.HTTP_201_CREATED)

@router.put('/update/{id}')
def update_produto(id:int, produto: Produto, db_session: Session = Depends(get_db_session)):
    uc = ProdutoUseCases(db_session=db_session)
    uc.update_produto(id=id, produto=produto)
    
    return Response(status_code=status.HTTP_200_OK)

@router.delete('/delete/{id}')
def delete_produto(id:int, db_session: Session = Depends(get_db_session)):
    
    uc = ProdutoUseCases(db_session=db_session)
    uc.delete_produto(id=id)
    
    return Response(status_code=status.HTTP_200_OK)