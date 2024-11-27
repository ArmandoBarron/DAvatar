import requests as api #for APIs request
import json
import time
import pickle
import statistics

url = 'http://148.247.202.72:5001/containers/container_9ab058ec4d29/extras/events/validated_contract?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI5ODMwNzgwfQ.1Ak5KfcZ7UkZNsBSoKikpr9trZGtTJyDleRtU6OvPiE'
result = api.get(url)
data = result.json()
print(data)

for i in range(0,20):
    url = 'http://148.247.202.72:5001/containers/container_9ab058ec4d29/extras/events/validated_contract?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI5ODMwNzgwfQ.1Ak5KfcZ7UkZNsBSoKikpr9trZGtTJyDleRtU6OvPiE'
    result = api.get(url)
    data = result.json() 
    print(data)

"""

start_time = time.time()
total_time = 0
r_t = []
while total_time < 100:
    response_time = time.time()
    result = api.get(url)
    data = result.json()
    #print(data)
    print("se hizo la petición")
    cv = 5
    print(cv)
    rr = time.time() - response_time
    r_t.append(rr)
    time.sleep(10)

    total_time = (time.time() - start_time)

summ = 0
for i in range(0,len(r_t)):
    summ = summ + r_t[i]

m_r_t = summ/len(r_t) 
s_r_t = statistics.stdev(r_t)
print("Requests: "+str(len(r_t)))
print("Median RT: "+str(m_r_t))
print("Standard RT: "+str(s_r_t))

print(r_t)

f = open("experiment_consume_case.txt", "a")
f.write("exp-case:"+str(m_r_t)+"-"+str(s_r_t)+"\n")
for element in r_t:
    f.write(str(element) + ",")
f.write("\n\n")

f.close()"""