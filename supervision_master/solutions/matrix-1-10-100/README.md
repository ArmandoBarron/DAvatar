Experiment on demand
========
1,10 solutions and 1,10 containers

## PLEASE RUN FROM PROTOTYPE

## Install
```bash
cd matrix-1-10-100

# build base image
docker build -t fbalderas/ida:base -f base-image/Dockerfile .

# up desired bash file; for example:
bash run-sol1c1.sh

# down desired bash file; for example:
bash down-sol1c1.sh
```
