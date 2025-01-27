FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 