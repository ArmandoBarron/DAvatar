FROM ubuntu:18.04-w-essentials

COPY ./bubble /home/bubble
WORKDIR /home/bubble
RUN gcc -pthread -o bubble bubble.c
