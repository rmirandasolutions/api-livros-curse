# API de livros

# GET, POST, PUT, DELETE

# POST - Adicionar novos livros - (Create)
# GET - Buscar os dados dos livros - (Read)
# PUT - Atualizar informações dos livros - (Update)
# DELETE - Deletar informações dos livros - (Delete)

#CRUD - Create, Read, Update, Delete
#Query strings - Parâmetros passados na URL após o "?" (ex: ?id=1&nome=livro)

# Documentação Swagger -> Documentar os endpoints da nossa API.

# Importamos o FastAPI para criar nossa API e o HTTPException para tratar erros HTTP.
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Puxa a URL do banco do arquivo .env ou usa o padrão local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./livros.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI(
    title="API de Livros",
    description="Uma simples API para gerenciar livros.",
    version="1.0.0",
    contact={
        "name": "Renan Miranda",
        "email": "rmirandasolutions@gmail.com"
    }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admin123"

security = HTTPBasic()

meus_livrozinhos = {} # Dicionário vazio que será usado temporariamente como armazenamento dos nossos livros.

# Definimos o modelo para os livros.
class LivroDB(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer, nullable=False)

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)  # Cria as tabelas no banco de dados, se ainda não existirem.

def sessao_db():
    """Função para criar uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    """Função para autenticar o usuário usando HTTP Basic Auth."""
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# ROTA GET
# @app.get() é um decorador que registra a função abaixo como responsável por requisições GET feitas para "/livros".
# GET -> Read -> Buscar/Ler informações
@app.get("/livros")
def get_livro(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Parâmetros de página e limite devem ser maiores que zero.")

    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()  # Consulta os livros no banco de dados com paginação.

    if not livros: # Se a lista de livros estiver vazia, significa que não há livros cadastrados.
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")

    total_livros = db.query(LivroDB).count()  # Conta o total de livros no banco de dados.

    return {
        "page": page,
        "limit": limit,
        "total_livros": total_livros,
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro} for livro in livros]  
    }


# ROTA POST
# @app.post() registra a função abaixo como responsável por requisições POST feitas para "/adiciona".
# POST -> Create -> Criar/Adicionar informações
@app.post("/adiciona")
def post_livros(livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == livro.nome_livro, LivroDB.autor_livro == livro.autor_livro).first()

    if db_livro:
        raise HTTPException(status_code=400, detail="Esse livro já existe no banco de dados.")

    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    return {"mensagem": "Livro adicionado com sucesso."}

# ROTA PUT
# {id_livro} é um parâmetro da URL usado para identificar qual livro deverá ser atualizado.
@app.put("/atualiza/{id_livro}")
def put_livro(id_livro: int, livro: Livro, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado no seu banco de dados.")
    
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro

    db.commit()
    db.refresh(db_livro)

    return {"mensagem": "Livro atualizado com sucesso."}

# ROTA DELETE
# {id_livro} identifica qual livro será deletado.
@app.delete("/deleta/{id_livro}")
def delete_livro(
    id_livro: int,  
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario),
    db: Session = Depends(sessao_db)
):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

    if not db_livro:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado no seu banco de dados.")

    db.delete(db_livro)
    db.commit()
    return {"mensagem": "Livro deletado com sucesso."}