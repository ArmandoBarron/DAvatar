FROM python:3.8.6-slim-buster
WORKDIR home

RUN pip install flask==2.3.0
RUN pip install Werkzeug==2.3.0
RUN pip install scikit-learn==1.0.1 
RUN pip install pandas --user

#RUN pip install pickle --user

COPY ./init.py init.py

ENTRYPOINT ["python"]
CMD ["init.py"]
