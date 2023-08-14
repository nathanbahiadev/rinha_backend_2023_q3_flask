FROM python:3.10

WORKDIR /app

ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update -y && apt-get install gcc musl-dev python3-dev -y

COPY requirements.txt .

RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000
