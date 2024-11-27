import requests as api #for APIs request
import json
# modify this id 
id_container = ""


json_object = {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "cluster1":1,"cluster2":2, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "cluster1":1,"cluster2":2, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "cluster1":2,"cluster2":2, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "cluster1":1,"cluster2":2, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "cluster1":1,"cluster2":2, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "cluster1":1,"cluster2":2, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "cluster1":1,"cluster2":2, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "cluster1":2,"cluster2":2, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],"columns":"cluster1,cluster2","method":"pearson"}

url = f'http://localhost:5001/containers/container_{id_container}/actions/correlation?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjE5OTMzNzA2fQ.mrL8po_iStRd0tyvvwqqyI-0a7ptzsJq3HeQ10o_RPs'
headers = {'Content-type': 'application/json'}
result = api.post(url, data=json.dumps(json_object),headers=headers)
print(result.text)
RES = result.json()
print(RES)