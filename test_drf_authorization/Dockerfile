FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY . .
