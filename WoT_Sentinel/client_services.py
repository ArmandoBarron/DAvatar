import requests as api #for APIs request
import json

#correlation
"""json_object = {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "cluster1":1,"cluster2":2, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "cluster1":1,"cluster2":2, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "cluster1":2,"cluster2":2, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "cluster1":1,"cluster2":2, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "cluster1":1,"cluster2":2, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "cluster1":1,"cluster2":2, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "cluster1":1,"cluster2":2, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "cluster1":2,"cluster2":2, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],"columns":"cluster1,cluster2","method":"pearson"}"""

#kmeans
json_object = {
        "K":3,
        "columns":"Temperature",
        "data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
        ]
    }

#melt
"""json_object = {"data":[
        {"Date": "2016-12-06", "Radiation":0.23, "test":-99, "Temperature": 0.7895, "Source": "GCAG"},
        {"Date": "2016-11-06", "Radiation":0.64, "test":-99, "Temperature": 0.7504, "Source": "GCAG"},
        {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
        {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
        {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
        {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
        {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
        {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"}],"id_vars":['Date'],"var_name":"Source","value_name":"value_test"}"""

#jaccard
"""json_object = {"data":[
    {"Date": "2016-12-06", "Radiation":0.23, "cluster1":1,"cluster2":2, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "cluster1":1,"cluster2":2, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "cluster1":2,"cluster2":2, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "cluster1":1,"cluster2":2, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "cluster1":1,"cluster2":2, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "cluster1":1,"cluster2":2, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "cluster1":1,"cluster2":2, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "cluster1":2,"cluster2":2, "Temperature": 1.3, "Source": "GISTEMP"} 
    ],"columns":"cluster1,cluster2"}"""

#silhouette
"""json_object = {
    "K":3,
    "columns":"Temperature",
    "data":[
    {"Date": "2016-12-06", "Radiation":0.23, "test":34, "Temperature": 0.7895, "Source": "GCAG"},
    {"Date": "2016-11-06", "Radiation":0.64, "test":30, "Temperature": 0.7504, "Source": "GCAG"},
    {"Date": "2016-10-06", "Radiation":0.18, "test":35, "Temperature": 0.7292, "Source": "GCAG"},
    {"Date": "2016-05-06", "Radiation":0.73, "test":30, "Temperature": 0.93, "Source": "GISTEMP"},
    {"Date": "2016-04-06", "Radiation":0.65, "test":24, "Temperature": 1.0733, "Source": "GCAG"},
    {"Date": "2016-04-06", "Radiation":0.61, "test":31, "Temperature": 1.09, "Source": "GISTEMP"},
    {"Date": "2016-03-06", "Radiation":0.53, "test":30, "Temperature": 1.2245, "Source": "GCAG"},
    {"Date": "2016-03-06", "Radiation":0.89, "test":11, "Temperature": 1.3, "Source": "GISTEMP"} 
    ]
}"""

#EXAMPLES ACTIONS:

#url = 'http://148.247.202.72:5001/containers/container_ea2ea3e7a61f/actions/correlation?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE2MTcyNzU1NTZ9.v0mj7wUdgU8nQqXVSBxIA5DvOUCZF5OZiSpfIGP9ihU'
#url = 'http://148.247.202.72:5001/containers/container_d143c45a98c2/actions/kmeans?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjE5MTcwNTkzfQ.C6_W_46swJFc3I_V9n9p8i3XTkx1dw3QD_CkDWcX-YM'
#url = 'http://148.247.202.72:5001:5001/containers/container_deb8dda60718/actions/melt?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE2MTcyNzU1NTZ9.v0mj7wUdgU8nQqXVSBxIA5DvOUCZF5OZiSpfIGP9ihU'
#url = 'http://148.247.202.72:5001/containers/container_509f9a14be10/actions/jaccard?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE2MTcyNzU1NTZ9.v0mj7wUdgU8nQqXVSBxIA5DvOUCZF5OZiSpfIGP9ihU'
#url = 'http://148.247.202.72:5001/containers/container_d143c45a98c2/actions/silhouette?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjE5MTcwNTkzfQ.C6_W_46swJFc3I_V9n9p8i3XTkx1dw3QD_CkDWcX-YM'

url = 'http://148.247.202.72:5001/containers/container_b0a86a4d9192/actions/kmeans?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjE5MTcwNTkzfQ.C6_W_46swJFc3I_V9n9p8i3XTkx1dw3QD_CkDWcX-YM'



#url = 'http://localhost:5000/containers/container_35b0d61e904c'
#url = 'http://localhost:5000/containers/container_3848bc8fc8de/actions/correlation'


#url = 'http://localhost:11001/clustering/kmeans'

#data = json_object['data']
# curl -g "http://localhost:54350"


headers = {'Content-type': 'application/json'}
result = api.post(url, data=json.dumps(json_object),headers=headers)
#result = api.post(url, data=json.dumps(data), params=(data_object) ,headers=headers)

#result = api.get(url, params=json.dumps(json_object))

#result = api.put(url,data=json.dumps(json_object))

#result = api.delete(url,params=json.dumps(json_object))

RES = result.json()
print(RES)



"""{'path': None, 'result': [
    {'Date': '2016-12-06', 'Radiation': 0.23, 'Source': 'GCAG', 'Temperature': 0.7895, 'class': 1, 'test': 34}, 
    {'Date': '2016-11-06', 'Radiation': 0.64, 'Source': 'GCAG', 'Temperature': 0.7504, 'class': 1, 'test': 30}, 
    {'Date': '2016-10-06', 'Radiation': 0.18, 'Source': 'GCAG', 'Temperature': 0.7292, 'class': 1, 'test': 35}, 
    {'Date': '2016-05-06', 'Radiation': 0.73, 'Source': 'GISTEMP', 'Temperature': 0.93, 'class': 0, 'test': 30}, 
    {'Date': '2016-04-06', 'Radiation': 0.65, 'Source': 'GCAG', 'Temperature': 1.0733, 'class': 0, 'test': 24}, 
    {'Date': '2016-04-06', 'Radiation': 0.61, 'Source': 'GISTEMP', 'Temperature': 1.09, 'class': 0, 'test': 31}, 
    {'Date': '2016-03-06', 'Radiation': 0.53, 'Source': 'GCAG', 'Temperature': 1.2245, 'class': 2, 'test': 30}, 
    {'Date': '2016-03-06', 'Radiation': 0.89, 'Source': 'GISTEMP', 'Temperature': 1.3, 'class': 2, 'test': 11}], 
    'status': 'OK'}"""