FROM python:3.9.12-slim-buster
WORKDIR /restaurant_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5008