#!/bin/bash
# Execution command: LOCALHOST=192.168.0.7 bash solutions/run-tps.sh
# Deploy tps manager and its services, also execute a pipeline with 5 stages
# load and preprocessing data, group the data, generate statistics, plot histograms, and clustering

SOLUTION=TPS

#

# deploy services
docker-compose -p TPS -f solutions/tps-manager/docker-compose.yml up -d
wait

# docker-compose -p prototype -f docker-compose.yml up -d
# wait

# execute with api, need this env variable
# LOCALHOST=192.168.0.7
docker-compose -p TPS -f solutions/tps-manager/STUDY-CASE/docker-compose.yml up -d
wait

# add solution
curl -G http://localhost:22000/replacesolution/TPS.yml/10/0/0
sleep 1

# steps of pipeline
# results are saved inside the container
curl -G http://localhost:54351/
curl --header "Content-Type: application/json" --request POST --data '{"source-folder":"Pollutants-data/20RAMA/"}' http://localhost:54351/load-data
curl -G http://localhost:54351/group-all-data
curl -G http://localhost:54351/statistics-by-column
curl -G http://localhost:54351/histograms-by-variable
curl -G http://localhost:54351/perform-clustering
sleep 2

# generate status and cards
# curl -G http://localhost:22004/v1/aggregates/TPS.yml/ALL/status-TPS-ALL
# curl -G http://localhost:22003/solution/model/wot-td/status/status-TPS-ALL
