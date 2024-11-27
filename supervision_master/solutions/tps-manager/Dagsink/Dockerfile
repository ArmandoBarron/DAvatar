FROM python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --user
RUN pip install Flask-API
RUN pip install socketIO-client
COPY app app
WORKDIR ./app

ENTRYPOINT ["python"]
CMD ["main.py"]
    