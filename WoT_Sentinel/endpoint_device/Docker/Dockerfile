#FROM ubuntu:18.04
#RUN apt-get update && apt-get install -y build-essential
#RUN apt-get -y install python3.7
#RUN apt-get update 
#RUN apt-get -y install python3.7-pip
#RUN apt-get update 
#RUN pip3 install flask
#FROM ubuntu:18.04
FROM python:3.8.6-slim-buster
RUN pip install flask==3.0.0
RUN pip3 install mysql-connector-python==8.0.29
RUN apt-get update
RUN pip3 install requests
RUN apt-get update
RUN pip3 install PyJWT==1.7.1
WORKDIR /home