# RestAPI com FastAPI

## Como executar em desenvolvimento (MacOS mas serve para outros SOs)
1. Criar um virtual environment com python 3.12.0 (ou outra versão compatível)
```bash
pyenv virtualenv 3.12.0 restapi
```
2. Ativar o ambiente virtual
```bash
pyenv activate restapi
```
3. Atualizar o pip
```bash
pyenv exec pip install --upgrade pip
```
4. Instalar o UV (alternativa ao pip, mais rápida)
```bash
pyenv exec pip install uv
```
5. Instalar as dependências
```bash
pyenv exec uv pip install -r requirements.txt --system
```
1. Iniciar o servidor
```bash
pyenv exec fastapi dev main.py
```
1. Entrar pelo browser em: http://localhost:8000

> [!TIP]
Para aceder à **documentação da API**, basta entrar em: http://localhost:8000/docs ou http://localhost:8000/redoc