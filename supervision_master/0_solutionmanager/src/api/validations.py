
def validate_model_services(services, services_model):
  invalid_services = []
  if services and services_model:
    for s in services.keys():
      if s not in services_model.keys():
        invalid_services.append(s)
  return invalid_services

def validate_model_structure(services_dict, structure_list):
  invalid_services = []
  if structure_list and len(structure_list)>0:
    for elem in structure_list:
      elem = elem.split('->')
      for e in elem:
        if e not in services_dict:
          invalid_services.append(e)
  return invalid_services


def validate_containers_raw(project_name, services_dict, containers_list):
  validated_containers = {}
  # TODO: find how many active containers corresponds to a container, not only the fist one
  for k, v in services_dict.items():
    temp_k = project_name+'_'+k
    cont_found = False
    for c in containers_list:
      # replicas = []
      if temp_k in c['name']:
        if len(temp_k) == len(c['name']):
          cont = c
          cont['service'] = k
          cont_found = True
          # cn = c['name']
          break
        elif len(temp_k)+2 <= len(c['name']):
          # Avoid false positive with similar names. Example: TPS_clustering, TPS_clustering_tools
          if temp_k == c['name'][:-2]:
            cont = c
            cont['service'] = k
            cont_found = True
            # cn = c['name']
            break
      elif v.get('container_name') and v.get('container_name') in c['name']:
        if v.get('container_name') == c['name']:
          cont = c
          cont['service'] = k
          cont_found = True
          # cn = c['name']
          break
          # TODO: else: add more validations to find correct service
    if not cont_found:
      cont = {'service': k}
    validated_containers[k] = cont
  return validated_containers