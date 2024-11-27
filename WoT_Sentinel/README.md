# Introduction
Below are the main concepts involved in this work:
- Virtual containers: these are pieces of software that provide a logical packaging mechanism in which applications can be abstracted from the environment in which they run.
- Web of Things: is a set of recommendations to uniquely and universally identify physical or abstract devices belonging to the Internet of Things. In such a way that all IoT devices can be connected to each other.
- Functional modeling: it is the representation of the behavior and function of a physical or abstract device. It allows you to describe devices as entities with a goal, and how their components contribute to achieving it.

# Deploy the system
The steps necessary to deploy the system on the host are shown below.

## Step 1 - Deploy Web service, ApiRest service, Database service

cd thesis_prototype <br>
docker-compose up -d

## Step 2 - Crerate config file
First you nedd to create the config file for your system. Below is an example of the structure it should have. Save the config file with the name of your system in representation/config_files with the extension ".cfg". It is important to know that it is necessary to define the names of the containers as they appear in docker. <br>

####################################################################
system-example
Example system for README.
-cont
container1-example
Container 1 example for README
-cont
container2-example
Container 2 example for README
--act
kmeans
Action example. It performs the grouping of the data using the kmeans algorithm. A class label is added to each record.
http://localhost:0000/kmeans
POST
---input
K
integer
Number of clusters.
---input
data
json
Json in record format with the data to be processed.
---output
result
json
Kmeans service result.
#####################################################################

Based on the previous example, the lines are explained in order:
- 1: Refers to the name of the system. No need to add dash.
- 2: Description of the system. No need to add dash.
- 3: Instruction that indicates that information from a container belonging to the system continues (instruction: "-cont").
- 4: Container name. No need to add dash.
- 5: Container description. No need to add dash.
- 6: Instruction that indicates that information from a container belonging to the system continues (instruction: "-cont").
- 7: Container name. No need to add dash.
- 8: Container description. No need to add dash.
- 9: Instruction that indicates that information of an action belonging to the container continues (instruction: "--act").
- 10: Action name. No need to add dash.
- 11: Action description. No need to add dash.
- 12: URI of the system that allows to consume the action. No need to add dash.
- 13: Consume type of the action (GET, POST, PUT, DELETE). No need to add dash.
- 14: Instruction that indicates that information from an input for the action continues (instruction: "---input").
- 15: Input name. No need to add dash.
- 16: Input type (string, integer, boolean, array, etc). No need to add dash.
- 17: Input description. No need to add dash.
- 18: Instruction that indicates that information from an input for the action continues (instruction: "---input").
- 19: Input name. No need to add dash.
- 20: Input type (string, integer, boolean, array, etc). No need to add dash.
- 21: Input description. No need to add dash.
- 22: Instruction that indicates that information from an output for the action continues (instruction: "---output").
- 23: Output name. No need to add dash.
- 24: Output type (string, integer, boolean, array, etc). No need to add dash.
- 25: Output description. No need to add dash.

## Step 3 - Model system and its containers
When the config file has already been created, you need to model the system and its containers. <br>

- First you need to change the name of your system in the file service_name.txt, make sure it is the same name as the one you write in the configuration file. <br>

- Second you need to execute model_application.py. Below is an example of how to run it.

cd thesis_prototype <br>
python3 representation/model_application.py <br>

## Step 4 - Consume the data
There are two ways to consume the data, one using the Web App that is mainly intended for the user, and another using the API REST service that is primarily intended for devices (virtual containers, sensors, etc.). Below are examples for the two ways (Web App, API REST). <br>

* Web App
http://localhost:8000/index.html 

* API REST
curl -G http://localhost:5001/containers/container_<id_container>/info <br>
curl -G http://localhost:5001/containers/container_<id_container>/entrypoint <br>

# Contact info
- mariana.hinojosa@cinvestav.mx
- hino.tije@gmail.com
- github: mariana_hiti