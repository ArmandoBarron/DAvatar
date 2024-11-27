#!/bin/bash

# INFO: Execute from prototype/

echo "deploy experiment sol1c10"
SOL_ID=1 docker-compose -p sol1c10 -f solutions/matrix-1-10-100/s1/c10/sol1c10.yml up -d

exit 0
