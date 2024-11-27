FROM python
WORKDIR home
COPY ./requeriments.txt requirements.txt

 
RUN pip install -r requirements.txt --user
RUN pip install Flask-API
RUN pip install socketIO-client
COPY app app
WORKDIR ./app
RUN export PYTHONPATH=$PWD:$PYTHONPATH 

ENTRYPOINT ["python"]
CMD ["main.py"]
