# FROM - fala ao Dockerfile que ele vai rodar uma aplicação Python.
# WORKDIR - fala ao container qual será o diretorio que a gente vai trabalhar.
# RUN - fala ao container pra ele qual comando rodar.
# COPY - copia os arquivos.
# RUN - fala pra ele que não é pra criar uma máquina virtual e instalar as dependencias.
# COPY - copia os restantes dos arquivos que estiverem no nosso diretorio.
# EXPOSE - expõe a porta 8000.
# CMD - comandos necessários para de fato o container ser executado pois até então é feita apenas a configuração desse container.

FROM python:3.14-slim 

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]