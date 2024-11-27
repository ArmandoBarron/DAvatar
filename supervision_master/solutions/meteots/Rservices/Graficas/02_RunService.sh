#!/bin/bash

docker run -d -it --name GraphsMet_0 -p 5500:5500 -v /home/robot/Escritorio/Projects/Servicios\ web/Diferencial/static/:/home/volumen/ graphs_meteo:v1
docker run -d -it --name GraphsMet_1 -p 5501:5500 -v /home/robot/Escritorio/Projects/Servicios\ web/Diferencial/static/:/home/volumen/ graphs_meteo:v1


