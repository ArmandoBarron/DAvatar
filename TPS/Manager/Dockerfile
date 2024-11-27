FROM python:3.8.6-slim-buster
WORKDIR home
RUN mkdir CONFIG
RUN mkdir SCHEMA

RUN pip install flask==2.3.0
RUN pip install Werkzeug==2.3.0


RUN pip install psycopg2-binary
RUN pip install configparser --user
RUN pip install requests --user
RUN pip install pandas --user
RUN pip install Flask-API --user
RUN pip install pymongo --user
RUN pip install flask-socketio
RUN pip install xlrd

COPY ./Tools Tools
COPY ./Services Services
COPY ./CONFIG CONFIG

COPY ./TPS-Manager.py TPS-Manager.py

ENTRYPOINT ["python"]
CMD ["TPS-Manager.py"]
