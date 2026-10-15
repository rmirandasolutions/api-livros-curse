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

## 🚀 Como Executar o Projeto

1. No terminal, execute o comando abaixo para construir as imagens e iniciar o container:

bash
docker compose up --build


## 🌐 Acessando a Aplicação

Após o container iniciar, acesse a documentação interativa da API (Swagger) no seu navegador através do link:

- **Documentação da API:** [http://localhost:8000/docs](http://localhost:8000/docs)