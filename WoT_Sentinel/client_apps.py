import requests as api #for APIs request
import json
import time
import pickle
import statistics

start_time = time.time()
total_time = 0
r_t = []
#json_object = {"sensor":"sensor0","generador":"generador"}
#url1 = 'http://148.247.202.72:5001/containers/container_3d1fa9ecf906/status?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
url1 = 'http://148.247.202.72:5001/containers/container_61d4b2b4fdce/network_utilization_low'
#url2 = 'http://10.0.0.5:5001/containers/container_7afb633a838e/network_utilization_low'
#url3 = 'http://10.0.0.5:5001/containers/container_734bd2e22360/network_utilization_low'
#url4 = 'http://10.0.0.5:5001/containers/container_e1954047a544/network_utilization_low'
#url5 = 'http://10.0.0.5:5001/containers/container_6d66681937b9/network_utilization_low'
headers = {'Content-type': 'application/json'}
while total_time < 60:
    
    #print(str(total_time))
    response_time = time.time()
    
    for i in range(0,25):
        result = api.get(url1)
        RES = result.json()

    """result = api.get(url1)
    RES = result.json()
    result = api.get(url1)
    RES = result.json()
    result = api.get(url1)
    RES = result.json()
    result = api.get(url1)
    RES = result.json()"""
    #print(RES)
 
    #result = api.get(url2)
    #RES = result.json()

    """result = api.get(url2)
    RES = result.json()
    result = api.get(url2)
    RES = result.json()
    result = api.get(url2)
    RES = result.json()
    result = api.get(url2)
    RES = result.json()"""
    #print(RES)
  
    #result = api.get(url3)
    #RES = result.json()

    """result = api.get(url3)
    RES = result.json()
    result = api.get(url3)
    RES = result.json()
    result = api.get(url3)
    RES = result.json()
    result = api.get(url3)
    RES = result.json()"""
    #print(RES)

    #result = api.get(url4)
    #RES = result.json()

    """result = api.get(url4)
    RES = result.json()
    result = api.get(url4)
    RES = result.json()
    result = api.get(url4)
    RES = result.json()
    result = api.get(url4)
    RES = result.json()"""
    #print(RES)

    #result = api.get(url5)
    #RES = result.json()

    """result = api.get(url5)
    RES = result.json()
    result = api.get(url5)
    RES = result.json()
    result = api.get(url5)
    RES = result.json()
    result = api.get(url5)
    RES = result.json()"""
    print(RES)

    rr = time.time() - response_time
    time.sleep(1)
    r_t.append(rr)

    total_time = (time.time() - start_time)

#print(str(total_time))
#print(r_t)

summ = 0
for i in range(0,len(r_t)):
    summ = summ + r_t[i]

m_r_t = summ/len(r_t) 
s_r_t = statistics.stdev(r_t)
print("Requests: "+str(len(r_t)))
print("Median RT: "+str(m_r_t))
print("Standard RT: "+str(s_r_t))

print(r_t)

f = open("experiment_consume_cpu.txt", "a")
f.write("exp-5-5_1s : "+str(m_r_t)+"-"+str(s_r_t)+"\n")
for element in r_t:
    f.write(str(element) + ",")
f.write("\n\n")

f.close()


"""start_time = time.time()
json_object = {"sensor":"sensor0","generador":"generador_1"}

#url = 'http://localhost:5055/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI1ODI4NjY1fQ.sCOaVC_m7-MraDnCXCe3Z-KITETa7lbx1VH8He6EOL4'

url = 'http://148.247.202.72:5001/containers/container_bb37026bd324/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDMzMjI3fQ.jSZG3SFTNkPubG_MM6n2EphRPNo4dwbHQBTDvEZS3ck'
headers = {'Content-type': 'application/json'}
result = api.post(url, data=json.dumps(json_object),headers=headers)

total_time = (time.time() - start_time)


RES = result.json()
print(RES)
print(str(total_time))


#token_endpoint_service = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDMzMjI3fQ.jSZG3SFTNkPubG_MM6n2EphRPNo4dwbHQBTDvEZS3ck"
#token_endpoint_wot = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI1ODI4NjY1fQ.sCOaVC_m7-MraDnCXCe3Z-KITETa7lbx1VH8He6EOL4" """