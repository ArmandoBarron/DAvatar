#!/bin/bash

# INFO: Execute from prototype/

echo "deploy experiment sol10c1"
for (( i = 1; i <= 10; i++ ))
do
    echo "deploy sol${i}c1"
    SOL_ID=$i docker-compose -p sol${i}c1 -f solutions/matrix-1-10-100/s10/c1/sol${i}c1.yml up -d
done

exit 0
