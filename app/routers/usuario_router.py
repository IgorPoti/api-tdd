from fastapi import status, Response, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
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
    

@router.post('/login')
def login_usuario(login_request_form: OAuth2PasswordRequestForm = Depends(),
                  db_session: Session = Depends(get_db_session)):
    
    uc = UsuarioUseCases(db_session=db_session)

    usuario = Usuario(
        nome=login_request_form.username,
        senha=login_request_form.password
    )
    
    token_data = uc.usuario_login(usuario=usuario, expires_in=60)
    
    return token_data