#!/bin/bash

# INFO: Execute from prototype/

for (( i = 1; i <= 10; i++ ))
do
    echo "remove sol${i}c10"
    SOL_ID=$i docker-compose -p sol${i}c10 -f solutions/matrix-1-10-100/s10/c10/sol${i}c10.yml down -v
done

exit 0