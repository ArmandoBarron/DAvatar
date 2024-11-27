#!/bin/bash

docker run -d -it --name ClustMet_0 -p 5400:5500 -v /home/robot/Escritorio/Projects/Servicios\ web/Diferencial/static/:/home/volumen/ clustering_meteo:v1



