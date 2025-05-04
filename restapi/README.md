# RestAPI with FastAPI

## How to run in development (MacOS but applicable to other OS)
1. Create a virtual environment with Python 3.12.0 (or another compatible version)
```bash
pyenv virtualenv 3.12.0 restapi
```
2. Activate the virtual environment
```bash
pyenv activate restapi
```
3. Update pip
```bash
pyenv exec pip install --upgrade pip
```
4. Install UV (alternative to pip, faster)
```bash
pyenv exec pip install uv
```
5. Install dependencies
```bash
pyenv exec uv pip install -r requirements.txt --system
```
6. Get the pre-built model (the .pt file) from the releases section https://github.com/Xurape/Food-Waste-Detection-using-YOLOv11/releases/latest/ and put it into the `/restapi/server/yolo/weights/` directory (Create it if it doesn't exist)
7. Start the server
```bash
pyenv exec fastapi dev main.py
```
8. Access via browser: http://localhost:8000

> [!TIP]
> To acess the **API documentation**, enter http://localhost:8000/docs or http://localhost:8000/redoc via browser.

> [!NOTE]
> To start the production server use docker.
