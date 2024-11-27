#!/bin/bash

# execution command: LHIP=192.168.0.20 LHPORT=8081 bash run-prototype.sh

# first deploy monitor agent
# ADMIN_USER=root ADMIN_PASSWORD=jupiter docker-compose -f monitor_agent/docker-compose.yml up -d

# then deploy supervision system
# docker-compose -p supervision -f docker-compose.yml up -d
ADMIN_USER=root ADMIN_PASSWORD=jupiter docker-compose -p supervision -f docker-compose.yml up -d

#docker-compose -p TPS -f solutions/tps-manager/docker-compose.yml up -d 
#docker-compose -p TPS -f tps.yml up -d 