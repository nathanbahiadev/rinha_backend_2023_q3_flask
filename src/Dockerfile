FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000
