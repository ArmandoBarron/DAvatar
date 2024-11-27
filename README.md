# DAvatar Deployment Guide

This document outlines the steps to deploy **DAvatar** and provides an example using a set of containers.

---

# Introduction
Below are the main concepts involved in this work:
- Virtual containers: these are pieces of software that provide a logical packaging mechanism in which applications can be abstracted from the environment in which they run.
- Web of Things: is a set of recommendations to uniquely and universally identify physical or abstract devices belonging to the Internet of Things. In such a way that all IoT devices can be connected to each other.
- Functional modeling: it is the representation of the behavior and function of a physical or abstract device. It allows you to describe devices as entities with a goal, and how their components contribute to achieving it.


## Requirements

Ensure the following are installed on your system:

- `python3.7` or higher
- `docker`
- `docker-compose`



## Component Deployment

To deploy and configure all components, follow these steps:

### Manual Deployment
Each component is contained within virtual containers. The specific steps for deployment are detailed in the README files located in the folders _*supervision_master*_ and _*WoT_Sentinel*_.

### Automated Deployment
For convenience, a script is provided to automate the deployment process.

1. Open the file _*run.sh*_ using a text editor.
2. Modify the IP address to match the local IP of the host machine.
3. If you are using WSL, follow the additional steps specified in the script's comments.

After making the necessary modifications, execute the following commands in your terminal:

```sh
    chmod +x ./run.sh
    ./run.sh
```
## Viewing the Digital Avatar

If all components have been deployed successfully, you can access the graphical interface to view the monitored components.

- **Version 1:** [http://localhost:8000/index.html](http://localhost:8000/index.html)
- **Version 2:** [http://localhost:22005/solutions/](http://localhost:22005/solutions/)



## Interacting with the Digital Avatar using WoT

You can interact with the monitored containers through the DAvatar interface using **WoT Cards**. To do this programmatically, follow these steps:

1. Navigate to the folder _*WoT_Sentinel*_:
```bash
   cd WoT_Sentinel
```
2. Open the file _*client_tpssummary.py*_ with a text editor.

3. Modify the `id` variable to match the corresponding container ID. You can find the container ID by visiting:
   [http://localhost:8000/apps_discovery.php](http://localhost:8000/apps_discovery.php)

4. Execute the script:
```bash
   python3 client_tpssummary.py
 ```

The console will display the result of the request, which is handled by the summary container.


# Contact info
* Juan Armando Barrón Lugo ([J.Armando Barrón-Lugo](https://orcid.org/my-orcid?orcid=0000-0002-9619-8116))
* Email: juan.barron@cinvestav.mx, juanbarronlugo@gmail.com
* GitHub: [@ArmandoBarron](https://github.com/ArmandoBarron)
* LinkedIn: [@Armando Barrón](https://www.linkedin.com/in/armando-barr%C3%B3n-52298310b) 
![Linkedin](https://i.stack.imgur.com/gVE0j.png)

# License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
