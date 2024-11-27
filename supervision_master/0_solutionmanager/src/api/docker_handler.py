import docker

def get_active_docker_containers(): 
  active_containers_list = []
  try:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    # TODO: specify docker host: tcp://127.0.0.1:1234
    if client:
      containers_list_obj = client.containers.list()
      client.close()
      if containers_list_obj:
        for c in containers_list_obj:
          json_cont = {
              "id": c.id,
              "name": c.name,
              "status": c.status
          }
          active_containers_list.append(json_cont)
  except:
    print('docker connection')
  return active_containers_list