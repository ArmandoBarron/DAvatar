#!/bin/bash

# INFO: Execute from prototype/

echo "deploy experiment sol1c1"
SOL_ID=1 docker-compose -p sol1c1 -f solutions/matrix-1-10-100/s1/c1/sol1c1.yml up -d

exit 0