
#env variables
IP_HOST="148.247.204.153"
MONITOR_FILE=run-prototype.sh #withouth wsl

#STEP 0 
#if your are using WSL, cadvisor will not work correctly. to solve this, we must first mount the docker-desktop-data into wsl
# if you are using WSL uncomment this steps. (do not execute this steps more than one time)
#####################################################

#sudo mkdir /mnt/docker-desktop-data #comment this after one exec
#sudo mount -t drvfs '\\wsl.localhost\docker-desktop\mnt\docker-desktop-disk\data\docker' /mnt/docker-desktop-data #comment this after one exec

#MONITOR_FILE=run-prototype-wsl.sh #but if you run this steps, you always need to use this file

#####################################################

# STEP 1. deploy the use case system (containers)
echo " "
echo "##################################### "
echo "############## STEP 1 ############### "
echo "##################################### "
echo " "

docker-compose -p tps -f tps.yml up -d 

# NOTE: make sure all the containers have been deployed

# STEP 2. run supervision master (with WoT v1.0)
echo " "
echo "##################################### "
echo "############## STEP 2 ############### "
echo "##################################### "
echo " "

cd supervision_master

IMAGE_NAME="fbalderas/python"
IMAGE_TAG="3.7-sb"  
# Verificar si la imagen existe
if [[ "$(docker images -q ${IMAGE_NAME}:${IMAGE_TAG} 2> /dev/null)" == "" ]]; then
  echo "Image ${IMAGE_NAME}:${IMAGE_TAG} not found. Building..."
  docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f base_image/DF_BaseImage ./base_image
else
  echo "Base image ${IMAGE_NAME}:${IMAGE_TAG} found."
fi

# run set of containers (all in the same machine)
bash $MONITOR_FILE
cd ..
# NOTE: supervision master can create an avatar by crawling the yml (tps.yml in this case). This yml is already allocated in supervision_master\0_solutionmanager\src\files, so we don't need to make any change to this. But if you want to add another set of containers you need to add the yml to this folder.


# STEP 3. run WoT sentinel ()
echo " "
echo "##################################### "
echo "############## STEP 3 ############### "
echo "##################################### "
echo " "

# verify if IP var is null
if [[ -z "$IP_HOST" ]]; then
  echo "IP_HOST getting local IP..."
  IP_HOST=$(ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)
else
  echo "IP_HOST : $IP_HOST"
fi

cd WoT_Sentinel/
export IP_HOST

docker-compose up -d
sleep 7
echo "init db... please wait"
sleep 8

#NOTE: please verify that all containers have been deloyed succesfully
echo " "
echo "##################################### "
echo "############## STEP 4 ############### "
echo "##################################### "
echo " "
## STEP 3.1 - Crerate config file
    # The Sentinel implementation can create WoT by a config file.
    # for this example (tps) the config file is already createad and allocated in WoT_Sentinel\representation\config_files\tps.cfg
    # the next step is register this cfg file into the sentinel DB (more details can bee seen in the WoT_Sentinel/readme.md file).

cd ./representation
python3 model_application.py #save model in database
# this step must be done just 1 time, for this reason, we are gonna change the name of the file
mv model_application.py DONE_model_application.py 


echo " "
echo "##################################### "
echo "############## STEP 5 ############### "
echo "##################################### "
echo " "
## STEP 3.2 - Start monitoring
cd ../listener/
python3 listener_run.py


# NOTE if you stop this script, you only need rerun the listener 


