# RestAPI com FastAPI

## Como executar em desenvolvimento
1. Criar um pyenv com python 3.12.0 (ou outra versão compatível)
```bash
pyenv install 3.12.0 # instalar o python 3.12.0
pyenv virtualenv 3.12.0 restapi # criar um ambiente virtual
```
2. Ativar o ambiente virtual
```bash
pyenv activate restapi
```
3. Instalar as dependências
```bash
pyenv exec pip install -r requirements.txt
```
4. Executar o servidor
```bash
pyenv exec fastapi dev main.py
```
5. Entrar pelo browser em: http://localhost:8000

