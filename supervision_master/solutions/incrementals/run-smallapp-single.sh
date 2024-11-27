#!/bin/bash
# Execution command: bash solutions/incrementals/run-smallapp-single.sh

SOLUTION=small-app
REPEAT=10
MINUTES=1
NSECONDS=$((60*$MINUTES))

for (( RP = 1; RP <= $REPEAT; RP++ )) ; do

    # deploy containers of the solution
    docker-compose -p $SOLUTION -f solutions/incrementals/$SOLUTION/docker-compose.yml up -d
    wait

    curl -G http://localhost:22000/replacesolution/$SOLUTION.yml/3/0/0

    # curl -G http://localhost:22001/monitor/stop/10
    # curl -X DELETE http://localhost:22002/solutions/$SOLUTION.yml/metrics/1
    # curl -X DELETE http://localhost:22000/times/clear

    # stop and remove containers of the solution
    # docker-compose -p $SOLUTION -f solutions/$SOLUTION/docker-compose.yml down
    # wait
    sleep $NSECONDS

    # generate status and cards
    # curl -G http://localhost:22004/v1/aggregates/$SOLUTION.yml/ALL/status-$SOLUTION-ALL
    # curl -G http://localhost:22003/solution/model/wot-td/status/status-$SOLUTION-ALL

done