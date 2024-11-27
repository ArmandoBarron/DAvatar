# Supervision Prototype
Title:

Método para la supervisión de sistemas de contenedores virtuales basado en multi-modelado

Abstract:

Los contenedores virtuales se han convertido en una solución popular para que las organizaciones solventen problemas de portabilidad, como encapsular una aplicación junto con sus dependencias sin que ésta se vea afectada por el entorno en que se ejecuta. Estos problemas son comunes en sistemas y patrones de software de entrega continua (los cuales deben proveer de manera constante la acción requerida), tales como tuberías de software o flujos de trabajo, ya que éstos comúnmente se ejecutan sobre entornos distribuidos. Garantizar la entrega continua de datos y/o metadatos a cada uno de los componentes de estos patrones y sistemas resulta crucial para este tipo de soluciones, los cuales deben hacer frente a riesgos potenciales que pueden afectar la continuidad del servicio que éstos proporcionan a los usuarios finales. Entre estos riesgos se encuentran afectaciones a propiedades de calidad, tales como eficiencia (que se ve disminuida en escenarios de sobrecarga de algún o algunos componentes), disponibilidad y resistencia a fallas o interrupciones parciales/totales de alguno de sus componentes. Para hacer frente a estos riesgos, es importante identificar los componentes que experimentan sobrecargas de trabajo y aquellos que presentan fallas y/o interrupciones de servicio. En esta tesis se propone solventar las deficiencias de los sistemas y patrones de entrega continua empleando un método de supervisión que permite identificar el punto de falla mediante una representación abstracta. La supervisión consiste en identificar, monitorear e indexar el estado de cada componente del sistema en cuestión, con base en aspectos no funcionales como eficiencia y confiabilidad. Para las tareas de supervisión se aplicó un enfoque de multi-modelado a los componentes del sistema, el cual consiste en combinar diferentes enfoques de abstracción como secuencial, funcional, estructural, entre otros. Este multi-modelado produce una representación abstracta de cada componente del sistema, lo que permite agilizar las tareas de supervisión. La evaluación experimental reveló la factibilidad de utilizar el método propuesto para la supervisión del estado en sistemas de contenedores virtuales.

Contact: fernando.balderas@cinvestav.mx

---

## Deploy the prototype
```bash
cd prototype
```
### Create base image
```bash
docker build -t fbalderas/python:3.7-sb -f base_image/DF_BaseImage ./base_image
```
### Deploy
```bash
bash run-prototype.sh
```
### Remove
```bash
bash down-prototype.sh
```
### Optional flags
```bash
# using monitor in different host, change the ip
LOCALHOST_IP=127.0.0.1
LOCALHOST_PORT=8080
# Dev only: It slows down over time causing overhead
CALCULATE_TIMES=1 # calculate service and response times
SAVE_DATASETS=1
```

## Adding solutions
### Study case TPS
```bash
# edit file, change the IP
nano solutions/tps-manager/Sourcefile.sourceme

# deploy
LOCALHOST=192.168.0.4 bash solutions/run-tps.sh
```
or
```bash
# edit file, change the IP
nano solutions/run-tps-rep.sh
# deploy and repeat
bash solutions/run-tps-rep.sh
```




## Enpoints v0.1

### add new solution
```bash
curl -G http://localhost:22000/addsolution/<solution.yml>/3/0/0
```
### add new solution overiding the old one
```bash
curl -G http://localhost:22000/replacesolution/<solution.yml>/3/0/0
#curl -G http://localhost:22000/replacesolution/tps.yml/3/1/0
#curl -G http://localhost:22000/replacesolution/app-example.yml/3/1/0
#curl -G http://localhost:22000/replacesolution/blockchain.yml/3/1/0
```
### get diagnosis with aggregates
```bash
curl -G http://localhost:22004/aggregates/<small-app.yml>/ALL/<status-small-app>
```
### get wot cards from previous aggregates
```bash
curl -X POST http://localhost:22003/model/wot-td/<status-solution>
```
### remove solution and its metrics
```bash
curl -X DELETE http://localhost:22002/solutions/<solution.yml>/metrics/<1>
```


## Enpoints v2
<!-- ### new solution
```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"solution": <solution.yml>, "monitor_interval": 3, "aggregates_interval": 20}' \
  http://localhost:22000/api/v2/solutions
``` -->
### get diagnosis with aggregates
```bash
curl -G http://localhost:22004/v2/aggregates/<solution.yml>/<BEGIN|END|Y-M-D-h-m-s>/<60>/<0>/<status-solution>
# example: curl -G http://localhost:22004/v2/aggregates/app-example.yml/END/60/0/status-app-example
```

## Additional endpoints
### count the samples saved for each metric
```bash
curl -G http://localhost:22002/dbs/datacube/collections/AggDocPerSecond_v1/count_documents
```
### count documents in a collection
```bash
curl -G http://localhost:22002/dbs/datacube/collections/<solutions>/count_documents
```
### quey n documents in a collection
```bash
curl -G http://localhost:22002/dbs/datacube/collections/<solutions>/documents/<2>
```
### get solution data
```bash
curl -G http://localhost:22002/solutions/<solution.yml>
```
<!-- ### Start/Stop monitoring background service
```bash
curl -G http://localhost:22001/monitor/{start|stop}/{10}
``` -->
### get monitoring raw stats of one container
```bash
curl -G http://localhost:22001/hosts/0/containers/<container_id>/<2>
```

### get structure
```bash
curl -G http://localhost:22003/model/structure/blockchain.yml
```

## for wsl mount docker-desktop-data folder in wsl

sudo mkdir docker-desktop-data
sudo mount -t drvfs '\\wsl.localhost\docker-desktop\mnt\docker-desktop-disk\data\docker' /mnt/aqui

