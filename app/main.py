from fastapi import FastAPI
from app.routers.categoria_router import router as categoria_router
from app.routers.produto_router import router as produto_router

app = FastAPI()
app.include_router(categoria_router)
app.include_router(produto_router)

