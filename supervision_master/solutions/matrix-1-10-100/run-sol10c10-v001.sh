#!/bin/bash

# INFO: Execute from prototype/

echo "deploy experiment sol10c10"
for (( i = 1; i <= 10; i++ ))
do
    echo "deploy sol${i}c10"
    SOL_ID=$i docker-compose -p sol${i}c10 -f solutions/matrix-1-10-100/s1/c10/docker-compose.yml up -d
done

exit 0