#!/bin/bash
# Execution command: bash solutions/run-tps-rep.sh
# Deploy tps manager and its services, also execute a pipeline with 5 stages
# load and preprocessing data, group the data, generate statistics, plot histograms, and clustering
# execution with api, need LOCALHOST env variable

SOLUTION=TPS
REPEAT=31
export LOCALHOST=192.168.0.2
source solutions/tps-manager/Sourcefile.sourceme


for (( RP = 1; RP <= $REPEAT; RP++ )) ; do
    # deploy services
    docker-compose -p TPS -f solutions/tps-manager/docker-compose.yml up -d
    wait
    sleep 1
    # docker-compose -p prototype -f docker-compose.yml up -d
    wait
    docker-compose -p TPS -f solutions/tps-manager/STUDY-CASE/docker-compose.yml up -d
    wait

    # add solution
    curl -G http://localhost:22000/replacesolution/TPS.yml/10/0/0

    # steps of pipeline
    # results are saved inside the container
    curl -G http://localhost:54351/
    curl --header "Content-Type: application/json" --request POST --data '{"source-folder":"Pollutants-data/15-19RAMA/"}' http://localhost:54351/load-data
    curl -G http://localhost:54351/group-all-data
    curl -G http://localhost:54351/statistics-by-column
    curl -G http://localhost:54351/histograms-by-variable
    curl -G http://localhost:54351/perform-clustering

    # # generate status and cards
    # curl -G http://localhost:22004/v1/aggregates/TPS.yml/ALL/status-TPS-ALL
    # curl -G http://localhost:22003/solution/model/wot-td/status/status-TPS-ALL

    sleep 10
    docker-compose -p TPS -f solutions/tps-manager/docker-compose.yml down -v
    wait
    # docker-compose -p prototype -f docker-compose.yml down -v
    wait
    # docker-compose -p TPS -f solutions/tps-manager/STUDY-CASE/docker-compose.yml down -v
    wait
done