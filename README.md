# Projeto Piloto - API de Livros - API básica para gerenciar livros

Este projeto foi desenvolvido e escalado como atividade prática e base para aprendizado e consolidação dos conteúdos no curso de Back-end Python.

## 🛠 Tecnologias Utilizadas

- **Python** (Linguagem base)
- **FastAPI** (Framework web)
- **Poetry** (Gerenciador de dependências e pacotes)
- **Docker & Docker Compose** (Conteinerização e orquestração)
- **Podman

## 📁 Estrutura Principal

- `main.py`: Código-fonte com a regra de negócio da API.
- `Dockerfile`: Receita de configuração do ambiente isolado da aplicação.
- `docker-compose.yml`: Orquestrador responsável por subir o container da aplicação.
- `pyproject.toml` e `poetry.lock`: Arquivos de controle das dependências do projeto.

## ⚙️ Variáveis de Ambiente

Antes de executar a aplicação, certifique-se de que o arquivo `.env` está presente na raiz do projeto com as seguintes variáveis configuradas:

```env
MEU_USUARIO=admin
MINHA_SENHA=admin123
DATABASE_URL=sqlite:///./livros.db
PYTHONUNBUFFERED=1

Como Executar o Projeto
Certifique-se de ter o Docker e Docker Compose instalados.

Na raiz do projeto, execute o comando:

Bash
docker compose up --build


## 🌐 Acessando a Aplicação

Após a inicialização do container, acesse a documentação interativa para testar as rotas (GET, POST, PUT, DELETE):

Swagger UI: http://localhost:8000/docs

Esse feedback mostra que a aplicação **já está subindo e funcionando no Docker** no computador do professor. Isso significa que a parte de conteinerização (Docker, Docker Compose, `.env`) foi um sucesso!

Agora, os 5 pontos restantes são ajustes rápidos de Python no `main.py`, a limpeza de uma pasta duplicada no GitHub e uma adição no `README.md`.

Vamos resolver cada um de forma bem simples:

---

### 1. Rota POST (Erro no cadastro do livro no `main.py`)

* **O problema:** Na hora de salvar o livro, o código está tentando usar o nome `db_livro`, mas a variável criada foi `novo_livro` (ou vice-versa).
* **Como arrumar:** No `main.py`, procure a função da rota `@app.post`. Veja o nome da variável que guarda o livro criado e garanta que `db.add(...)`, `db.commit()` e `db.refresh(...)` usem a **mesma variável**.

Exemplo de como deve ficar:

```python
@app.post("/livros")
def criar_livro(livro: LivroSchema, db: Session = Depends(get_db)):
    novo_livro = Livro(**livro.dict()) # nome da variável
    db.add(novo_livro)                 # usa novo_livro
    db.commit()
    db.refresh(novo_livro)            # usa novo_livro
    return novo_livro

```

---

### 2. Rota PUT (Erro de indentação no `main.py`)

* **O problema:** As linhas de código que atualizam o livro ficaram indentadas (empurradas para a direita) para dentro do bloco de erro `raise HTTPException(...)`. Por isso, a função para no erro e nunca executa a atualização.
* **Como arrumar:** No `main.py`, procure a rota `@app.put`. Garanta que o trecho que altera os campos do livro esteja no mesmo nível de recuo do `if`, e **não** dentro do `if`.

Exemplo de como deve ficar:

```python
@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro: LivroSchema, db: Session = Depends(get_db)):
    livro_db = db.query(Livro).filter(Livro.id == livro_id).first()
    
    if not livro_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Estas linhas devem ficar FORA do 'if' (no mesmo nível da margem):
    livro_db.titulo = livro.titulo
    livro_db.autor = livro.autor
    db.commit()
    db.refresh(livro_db)
    return livro_db

```

---

### 3. Rota DELETE (Falta a sessão `db` no `main.py`)

* **O problema:** A rota de deletar tenta usar a variável `db`, mas o parâmetro `db` não foi passado nos parênteses da função.
* **Como arrumar:** No `main.py`, procure a rota `@app.delete` e insira o parâmetro `db: Session = Depends(get_db)` dentro dos parênteses da função.

Exemplo de como deve ficar:

```python
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)): # <--- Adicione db: Session...
    livro_db = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(livro_db)
    db.commit()
    return {"message": "Livro deletado com sucesso"}

```

---

### 4. Organização no GitHub (Remover a pasta duplicada)

* **O problema:** Há uma subpasta com o nome `PROJETO-CURSO-BACKEND-LIVROS-PYTHON` dentro do seu repositório contendo uma cópia dos arquivos antigos.
* **Como arrumar:**
1. Acesse seu repositório no GitHub pelo navegador.
2. Clique para entrar na subpasta `PROJETO-CURSO-BACKEND-LIVROS-PYTHON`.
3. No canto superior direito da lista de arquivos dessa pasta, clique nos três pontinhos (`...`) ou entre na pasta e escolha **Delete directory** (ou apague os arquivos de dentro dela).
4. Garanta que os arquivos corretos estejam **apenas na raiz do repositório** (fora de qualquer subpasta).



---

### 5. Atualizar o `README.md`

Adicione um pequeno trecho no `README.md` explicando o arquivo `.env`. Substitua a seção de execução no seu README por esta:

```md
## ⚙️ Variáveis de Ambiente

Antes de executar a aplicação, certifique-se de que o arquivo `.env` está presente na raiz do projeto com as seguintes variáveis configuradas:

```env
MEU_USUARIO=admin
MINHA_SENHA=admin123
DATABASE_URL=sqlite:///./livros.db
PYTHONUNBUFFERED=1

```

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Na raiz do projeto, execute o comando:

```bash
docker compose up --build

```

## 🌐 Acessando a Aplicação

Após a inicialização do container, acesse a documentação interativa para testar as rotas (GET, POST, PUT, DELETE):

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

Esse feedback mostra que a aplicação **já está subindo e funcionando no Docker** no computador do professor. Isso significa que a parte de conteinerização (Docker, Docker Compose, `.env`) foi um sucesso!

Agora, os 5 pontos restantes são ajustes rápidos de Python no `main.py`, a limpeza de uma pasta duplicada no GitHub e uma adição no `README.md`.

Vamos resolver cada um de forma bem simples:

---

### 1. Rota POST (Erro no cadastro do livro no `main.py`)

* **O problema:** Na hora de salvar o livro, o código está tentando usar o nome `db_livro`, mas a variável criada foi `novo_livro` (ou vice-versa).
* **Como arrumar:** No `main.py`, procure a função da rota `@app.post`. Veja o nome da variável que guarda o livro criado e garanta que `db.add(...)`, `db.commit()` e `db.refresh(...)` usem a **mesma variável**.

Exemplo de como deve ficar:

```python
@app.post("/livros")
def criar_livro(livro: LivroSchema, db: Session = Depends(get_db)):
    novo_livro = Livro(**livro.dict()) # nome da variável
    db.add(novo_livro)                 # usa novo_livro
    db.commit()
    db.refresh(novo_livro)            # usa novo_livro
    return novo_livro

```

---

### 2. Rota PUT (Erro de indentação no `main.py`)

* **O problema:** As linhas de código que atualizam o livro ficaram indentadas (empurradas para a direita) para dentro do bloco de erro `raise HTTPException(...)`. Por isso, a função para no erro e nunca executa a atualização.
* **Como arrumar:** No `main.py`, procure a rota `@app.put`. Garanta que o trecho que altera os campos do livro esteja no mesmo nível de recuo do `if`, e **não** dentro do `if`.

Exemplo de como deve ficar:

```python
@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro: LivroSchema, db: Session = Depends(get_db)):
    livro_db = db.query(Livro).filter(Livro.id == livro_id).first()
    
    if not livro_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Estas linhas devem ficar FORA do 'if' (no mesmo nível da margem):
    livro_db.titulo = livro.titulo
    livro_db.autor = livro.autor
    db.commit()
    db.refresh(livro_db)
    return livro_db

```

---

### 3. Rota DELETE (Falta a sessão `db` no `main.py`)

* **O problema:** A rota de deletar tenta usar a variável `db`, mas o parâmetro `db` não foi passado nos parênteses da função.
* **Como arrumar:** No `main.py`, procure a rota `@app.delete` e insira o parâmetro `db: Session = Depends(get_db)` dentro dos parênteses da função.

Exemplo de como deve ficar:

```python
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)): # <--- Adicione db: Session...
    livro_db = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    db.delete(livro_db)
    db.commit()
    return {"message": "Livro deletado com sucesso"}

```

---

### 4. Organização no GitHub (Remover a pasta duplicada)

* **O problema:** Há uma subpasta com o nome `PROJETO-CURSO-BACKEND-LIVROS-PYTHON` dentro do seu repositório contendo uma cópia dos arquivos antigos.
* **Como arrumar:**
1. Acesse seu repositório no GitHub pelo navegador.
2. Clique para entrar na subpasta `PROJETO-CURSO-BACKEND-LIVROS-PYTHON`.
3. No canto superior direito da lista de arquivos dessa pasta, clique nos três pontinhos (`...`) ou entre na pasta e escolha **Delete directory** (ou apague os arquivos de dentro dela).
4. Garanta que os arquivos corretos estejam **apenas na raiz do repositório** (fora de qualquer subpasta).



---

### 5. Atualizar o `README.md`

Adicione um pequeno trecho no `README.md` explicando o arquivo `.env`. Substitua a seção de execução no seu README por esta:

```md
## ⚙️ Variáveis de Ambiente

Antes de executar a aplicação, certifique-se de que o arquivo `.env` está presente na raiz do projeto com as seguintes variáveis configuradas:

```env
MEU_USUARIO=admin
MINHA_SENHA=admin123
DATABASE_URL=sqlite:///./livros.db
PYTHONUNBUFFERED=1

```

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Na raiz do projeto, execute o comando:

```bash
docker compose up --build

```

## 🌐 Acessando a Aplicação

Após a inicialização do container, acesse a documentação interativa para testar as rotas (GET, POST, PUT, DELETE):

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)


```
Após fazer essas edições no seu computador, faça o upload dos arquivos atualizados para o GitHub usando a opção **Add file > Upload files** e faça o commit. Com esses ajustes na lógica da API e a limpeza da pasta duplicada, seu projeto estará finalizado!

```