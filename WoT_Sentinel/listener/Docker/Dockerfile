FROM ubuntu:18.04
RUN apt-get update && apt-get install -y build-essential
RUN apt-get -y install python3
RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get update
RUN pip3 install mysql-connector-python
WORKDIR /home

#docker build -f solutions/incrementals/net-app/app/Dockerfile -t net-app_img .