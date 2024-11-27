#!/bin/bash

# execution command: bash down-prototype.sh

# first remove supervision system
docker-compose -p supervision -f docker-compose.yml down

# then remove monitor agent
# docker-compose -f monitor_agent/docker-compose.yml down
