from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    produtos = relationship('Produtos', back_populates='categoria')
    

class Produtos(Base):
    __tablename__ = "produtos"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    preco = Column('preco', Float)
    quantidade = Column('quantidade', Integer)
    created_at = Column('created_at', DateTime, server_default=func.now())
    updated_at = Column('updated_at', DateTime, onupdate=func.now())
    categoria_id = Column('categoria_id', ForeignKey('categorias.id'), nullable=False)
    categoria = relationship('Categoria', back_populates='produtos')
