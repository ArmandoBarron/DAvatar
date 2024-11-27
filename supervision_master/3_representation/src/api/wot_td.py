from pyld import jsonld

def make_wot_td_card(cv_name, m_info, u_cpu, u_fs, u_mem, u_net):
  
  cid = m_info.get('id')
  fun = m_info.get('functions')
  inp = m_info.get('input')
  out = m_info.get('output')
  wtd = 'https://www.w3.org/2019/wot/td'
  ctv = 'https://www.tamps.cinvestav.mx/schema'

  input_schema = {
      "@type": "string", 
      wtd + "#description" : "Shows the input of the Thing",
    }
  if inp:
    if inp.get('description') and inp.get('description') != '':
      input_schema[wtd + '#description'] = inp.get('description')
    if inp.get('elements') and type(inp.get('elements')) is list:  
      for elem in inp.get('elements'):
        if type(elem) is dict:
          for k in elem:
            input_schema[ctv + '/' + k] = elem[k]
        
  output_schema = {
      "@type": "string", 
      wtd + "#description" : "Shows the output of the Thing",
    }
  if out:
    if out.get('description') and out.get('description') != '':
      output_schema[wtd + '#description'] = out.get('description')
    if out.get('elements') and type(out.get('elements')) is list:
      for elem in out.get('elements'):
        if type(elem) is dict:
          for k in elem:
            output_schema[ctv + '/'+k] = elem[k]
    
  behavior = {
    "@type": "string",
    wtd + "#description" : "Shows params about the behavior of the Thing",
    ctv + "/cpu_util": {
      "@type": "number", 
      ctv + "/util": u_cpu,
      "https://www.w3.org/2019/wot/json-schema#readOnly": True,
      wtd + "#description" : "Shows the cpu utilization of the Thing",
    },
    ctv + "/filesystem_util": {
      "@type": "number",
      ctv + "/util": u_fs,
      "https://www.w3.org/2019/wot/json-schema#readOnly": True,
      wtd + "#description" : "Shows the filesystem utilization of the Thing",
    },
    ctv + "/memory_util": {
      "@type": "number",
      ctv + "/util": u_mem,
      "https://www.w3.org/2019/wot/json-schema#readOnly": True,
      wtd + "#description" : "Shows the memory utilization of the Thing",
    },
    ctv + "/network_util": {
      "@type": "number",
      ctv + "/util": u_net,
      "https://www.w3.org/2019/wot/json-schema#readOnly": True,
      wtd + "#description" : "Shows the network utilization of the Thing",
    }
  }

  property_aff = {
    ctv + "/structure": {
      "@type": "string",
      wtd + "#description" : "Shows params about the structure of the Thing",
      wtd + "#hasInputSchema": input_schema,
      wtd + "#hasOutputSchema": output_schema
    },
    ctv + "/behavior": behavior
  }
    
  action_aff = {}
  if fun:
    if type(fun) is dict and len(fun) == 1:
      for k in fun:
        action_aff[ctv + '/'+k] = {
            wtd + "#forms": [{
                wtd + "#description" : fun[k][0],
                wtd + "#href": fun[k][1]
              }]
          }
    elif type(fun) is list:
      for elem in fun:
        if type(elem) is dict and len(elem) == 1:
          for k in elem:
            action_aff[ctv + '/'+k] = {
                wtd + "#forms": [{
                    wtd + "#description" : fun[k][0],
                    wtd + "#href": fun[k][1]
                  }]
              }

  event_aff = {
    ctv + "/CPULowThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/cpu_lth",
      }]
    },
    ctv + "/FSLowThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/fs_lth",
      }]
    },
    ctv + "/MEMLowThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/mem_lth",
      }]
    },
    ctv + "/NETLowThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/net_lth",
      }]
    },
    ctv + "/CPUMediumThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/cpu_mth",
      }]
    },
    ctv + "/FSMediumThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/fs_mth",
      }]
    },
    ctv + "/MEMMediumThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/mem_mth",
      }]
    },
    ctv + "/NETMediumThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/net_mth",
      }]
    },
    ctv + "/CPUHighThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/cpu_hth",
      }]
    },
    ctv + "/FSHighThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/fs_hth",
      }]
    },
    ctv + "/MEMHighThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/mem_hth",
      }]
    },
    ctv + "/NETHighThreshold":{
      wtd + "#data": {"@type": "bool"},
      wtd + "#forms": [{
        wtd + "#href": "https://thing.example.com/net_hth",
      }]
    },
  }

  context = [
    wtd + "/v1",
    {
      "@version": 1.1,
      "@language" : "en",
      "ctv": ctv + "/",
      "utilization": {"@id": "ctv:util", "@type": "jsonschema:NumberSchema"},
    }
  ]
  doc = {
    "@id": "http://www.tamps.cinvestav.mx/" + cid,
    "@type": wtd + "#Thing",
    wtd + "#title": cv_name,
    wtd + "#description": m_info.get('description'),
    wtd + "#hasPropertyAffordance": property_aff,
    wtd + "#hasActionAffordance":  action_aff,
    wtd + "#hasEventAffordance": event_aff
  }
  # TODO: download wot context to solve error while offline
  try:
    card = jsonld.compact(doc, context)
  except:
    print('Error compacting jsonld')
    card = {}
  
  return card
