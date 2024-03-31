from fastapi import status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from app.routers.deps import get_db_session
from app.schemas.usuario import Usuario
from app.use_cases.usuario import UsuarioUseCases

router = APIRouter(prefix='/usuario')

@router.post('/registrar')
def registrar_usuario(usuario:Usuario, db_session: Session = Depends(get_db_session)):
    
    uc = UsuarioUseCases(db_session=db_session)
    uc.registrar_usuario(usuario=usuario)
    return Response(status_code=status.HTTP_201_CREATED)
    
    