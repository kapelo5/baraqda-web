# syntax=docker/dockerfile:1
FROM debian:jessie

FROM python:3.8-bullseye

RUN apt-get update -y && apt-get upgrade -y && apt-get install git -y

RUN useradd -ms /bin/bash bar_user
USER bar_user
WORKDIR /baraqda-web

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV FLASK_APP index.py
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
