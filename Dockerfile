FROM python:3.8

COPY ./backend /backend
WORKDIR /backend

RUN pip install -r requirements.txt