#!/bin/bash

# Execution command:

docker rmi -f prototype_representation
docker rmi -f prototype_consumer
docker rmi -f prototype_web
docker rmi -f prototype_diagnosis
docker rmi -f prototype_solution_mgr
docker rmi -f prototype_monitoring
docker rmi -f prototype_indexing
docker rmi -f fbalderas/python:3.7-sb

docker build -t fbalderas/python:3.7-sb -f base_image/DF_BaseImage ./base_image
