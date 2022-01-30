FROM ubuntu:20.04

COPY requirements.txt /requirements.txt

RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip -y


RUN pip install -r /requirements.txt

COPY ./app /opt/app

EXPOSE 5000
WORKDIR /opt/

ENTRYPOINT python3 app/back/app.py