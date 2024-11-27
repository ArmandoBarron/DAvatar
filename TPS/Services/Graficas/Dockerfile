FROM python:3.8.6-slim-buster

ADD ./app /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 7070

ENTRYPOINT [ "python3", "/app/app.py" ]
