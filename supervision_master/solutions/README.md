# Solutions

Note: Run from supervision/






## Incrementals
### Small-app 
```bash
# create base image
docker build -t ubuntu:18.04-w-essentials -f solutions/incrementals/small-app/base-image/Dockerfile ./solutions/incrementals/small-app
# run experiment
bash solutions/incrementals/run-smallapp-single.sh
```

### IDA
```bash
# REQUIERE IDA:BASE from IDA multiworkers
# first create folders and generate file
mkdir solutions/incrementals/ida/Code/files 
mkdir solutions/incrementals/ida/Code/files_recovered
# head -c 1M </dev/urandom > solutions/incrementals/ida/Code/files/1MB.txt
head -c 10M </dev/urandom > solutions/incrementals/ida/Code/files/10MB.txt
head -c 100M </dev/urandom > solutions/incrementals/ida/Code/files/100MB.txt
head -c 1000M </dev/urandom > solutions/incrementals/ida/Code/files/1000MB.txt
# run experiment
bash solutions/incrementals/run-ida-single.sh
```



## Concurrents
### IDA
```bash
# REQUIERE IDA:BASE from IDA multiworkers
# first create folders and generate file
mkdir solutions/concurrents/ida/Code/files 
mkdir solutions/concurrents/ida/Code/files_recovered
head -c 10M </dev/urandom > solutions/concurrents/ida/Code/files/10MB.txt
head -c 100M </dev/urandom > solutions/concurrents/ida/Code/files/100MB.txt
head -c 1000M </dev/urandom > solutions/concurrents/ida/Code/files/1000MB.txt
# run experiment
bash solutions/concurrents/run-ida-single.sh
```

### Small-app 
```bash
# create base image
docker build -t ubuntu:18.04-w-essentials -f solutions/concurrents/small-app/base-image/Dockerfile ./solutions/concurrents/small-app
# run experiment
bash solutions/concurrents/run-smallapp-single.sh
```




## Repetitives
## Small-app example
### Run a solution
```bash
docker build -t ubuntu:18.04-w-essentials -f solutions/repetitives/small-app/base-image/Dockerfile ./solutions/repetitives/small-app
docker-compose -p small-app-rep -f solutions/repetitives/small-app/docker-compose.yml up -d
curl -G http://localhost:22000/addsolution/small-app-rep.yml/10/1/0
curl -G http://localhost:22004/v2/aggregates/small-app-rep.yml/BEGIN/1/1/status-small-app-rep
curl -G http://localhost:22003/solution/model/wot-td/status/status-small-app-rep
```

### IDA multiworkers simple app example
```bash
# first create folders and generate file
mkdir solutions/repetitives/ida/Code/files 
mkdir solutions/repetitives/ida/Code/files_recovered
head -c 500M </dev/urandom > solutions/repetitives/ida/Code/files/file.txt
# openssl rand -out solutions/repetitives/ida/Code/files/file.txt -base64 $(( 2**29 * 3/4 ))
docker build -t fbalderas/ida:base -f solutions/repetitives/ida/base-image/Dockerfile ./solutions/repetitives/ida
docker-compose -p ida -f solutions/repetitives/ida/docker-compose.yml up -d
curl -G http://localhost:22000/addsolution/ida.yml/10/1/0
curl -G http://localhost:22004/v2/aggregates/ida.yml/BEGIN/10/1/status-ida
curl -G http://localhost:22003/solution/model/wot-td/status/status-ida
```

### Kulla master-slave app example
```bash
# first generate files of dataset
cd solutions/repetitives/kulla
python3 generate-files.py -s 200M -n 32 -p ~/prototype/solutions/repetitives/kulla/MasterSlave/Volume/Source
python2 generate-files.py -s 200M -n 32 -p ~/prototype/solutions/repetitives/kulla/MasterSlave/Volume/Source
mkdir MasterSlave/Volume/Sink
cd ~/prototype
docker-compose -p kulla -f solutions/repetitives/kulla/docker-compose.yml up -d
curl -G http://localhost:22000/addsolution/kulla.yml/10/1
curl -G http://localhost:22004/v2/aggregates/kulla.yml/BEGIN/10/1/status-kulla
curl -G http://localhost:22003/solution/model/wot-td/status/status-kulla
```


### Matrix of IDA apps example
```bash
# first create folders and generate file
mkdir solutions/matrix-1-10-100/ida-code/input
mkdir solutions/matrix-1-10-100/ida-code/output
head -c 100M </dev/urandom > solutions/matrix-1-10-100/ida-code/input/file.txt

# build base image if not exist
docker build -t fbalderas/ida:base -f solutions/matrix-1-10-100/base-image/Dockerfile ./solutions/matrix-1-10-100
bash solutions/run-matrix-v3.sh -e 4 -m 1 -r 1 -p experiments/11-1-matrix/tests-dell/4-2-2_1
# maybe use nohup
```






## Meteo example
### Run a solution
```bash
# first change config.ini
docker-compose -p meteots -f solutions/meteots/docker-compose.yml up -d
# also can use
# cd solutions/meteots
# docker-compose up -d
docker-compose -p consumer -f consumer/docker-compose.yml up -d
# Note: consumer moved to experiments/
curl -G http://localhost:22011/consumer/start
# curl -G http://localhost:22011/consumer/{start|stop}
curl -G http://localhost:22000/addsolution/meteots.yml/1/1
```
