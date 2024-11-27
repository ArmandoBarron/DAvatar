#!/bin/bash
# Execution command: bash solutions/concurrents/run-smallapp-single.sh

SOLUTION=small-app
REPEAT=31
MINUTES=2
NSECONDS=$((60*$MINUTES))

for (( RP = 1; RP <= $REPEAT; RP++ )) ; do

    # deploy containers of the solution
    docker-compose -p $SOLUTION -f solutions/concurrents/$SOLUTION/docker-compose.yml up -d
    wait

    curl -G http://localhost:22010/replacesolution/$SOLUTION.yml/3/1/0

    sleep $NSECONDS

done