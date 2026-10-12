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

Certifique-se de ter o [Docker](https://www.docker.com/) instalado na sua máquina.

1. Navegue até a pasta raiz do projeto.
2. No terminal, execute o comando abaixo para construir e iniciar o container:

bash
docker compose up --b


3. Aguarde a finalização da montagem da imagem e o servidor iniciar.

## 🌐 Acessando a Aplicação

Com o container rodando, a API estará acessível localmente. Você pode interagir com ela e visualizar a aplicação acessando o link abaixo no seu navegador:

- **Documentação / Testes:** [http://localhost:8000](http://localhost:8000)