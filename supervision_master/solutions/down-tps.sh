#!/bin/bash
# Execution command: bash solutions/down-tps.sh
# copy and paste in terminal
# execute from prototype/

# docker-compose down -v
docker-compose -p TPS -f solutions/tps-manager/docker-compose.yml down -v
docker-compose -p TPS -f solutions/tps-manager/STUDY-CASE/docker-compose.yml down -v
