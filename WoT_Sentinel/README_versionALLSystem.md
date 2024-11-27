# Introduction
Hello, my name is Mariana Hinojosa Tijerina, the title of my work is *Functional modeling for Docker virtual containers*.

Below are the main concepts involved in this work:
- Virtual containers: these are pieces of software that provide a logical packaging mechanism in which applications can be abstracted from the environment in which they run.
- Web of Things: is a set of recommendations to uniquely and universally identify physical or abstract devices belonging to the Internet of Things. In such a way that all IoT devices can be connected to each other.
- Functional modeling: it is the representation of the behavior and function of a physical or abstract device. It allows you to describe devices as entities with a goal, and how their components contribute to achieving it.

# Deploy the system
The steps necessary to deploy the system on the host are shown below.

## Step 1 - Deploy Web service, ApiRest service, Database service

cd thesis_prototype <br>
docker-compose up -d

## Step 2 - Deploy Listener service 

cd thesis_prototype <br>
nohup python3 listener/listener_run.py &

nohup python3 endpoint/endpoint_WoT.py &

nohup python3 check_resources.py &

## Step 3 - Model containers and application
First you need to model the containers that your application contains and then model the application <br>

cd thesis_prototype <br>
python3 model_container.py           *for each of the containers* <br>
python3 model_app.py                 *for the application* <br>

## Step 4 - Consume the data
There are two ways to consume the data, one using the Web service that is mainly intended for the user, and another using the ApiRest service that is primarily intended for devices (virtual containers, sensors, etc.) <br>

* Web service
http://localhost:8000/index.html 

* ApiRest service
curl -G http://localhost:5000/containers/container_<id_container> <br>
curl -G http://localhost:5000/applications/app_<name_of_application>

# Contact info
- mariana.hinojosa@cinvestav.mx
- hino.tije@gmail.com
- github: mariana_hiti

curl -G http://localhost:5000/containers/container_d38d7952acc1/info

# Run endpoint_wot (on blockchain project)
cd blockchain 
nohup python3 endpoint/endpoint_WoT.py > log.txt 2>&1 &