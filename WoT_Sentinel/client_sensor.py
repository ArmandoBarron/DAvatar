import requests as api #for APIs request
import json
import time
import pickle
import statistics

start_time = time.time()
total_time = 0
r_t = []
json_object = {"sensor":"sensor0","generador":"generador"}
url1 = 'http://148.247.202.72:5001/containers/container_4788f98fc2ee/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
url2 = 'http://148.247.202.72:5001/containers/container_cc731c5e1738/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
url3 = 'http://148.247.202.72:5001/containers/container_c8dc366e881b/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
url4 = 'http://148.247.202.72:5001/containers/container_08df0aa55893/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
url5 = 'http://148.247.202.72:5001/containers/container_c5da7c161f35/actions/show_data?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs'
headers = {'Content-type': 'application/json'}
while total_time < 600:
    
    #print(str(total_time))
    response_time = time.time()
    result = api.post(url1, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url1, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url1, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)

    result = api.post(url2, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url2, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url2, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)


    result = api.post(url3, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url3, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url3, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)

    result = api.post(url4, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url4, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url4, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)

    result = api.post(url5, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url5, data=json.dumps(json_object),headers=headers)
    RES = result.json()
    print(RES)
    result = api.post(url5, data=json.dumps(json_object),headers=headers)
    RES = result.json()
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

f = open("experiment_consume_2.txt", "a")
f.write("exp-5-5_1:"+str(m_r_t)+"-"+str(s_r_t)+"\n")
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