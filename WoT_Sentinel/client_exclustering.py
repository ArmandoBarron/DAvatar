import requests as api #for APIs request
import json
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
url = 'http://localhost:5001/containers/container_d143c45a98c2/actions/kmeans?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjE5OTMzNzA2fQ.mrL8po_iStRd0tyvvwqqyI-0a7ptzsJq3HeQ10o_RPs'
headers = {'Content-type': 'application/json'}
result = api.post(url, data=json.dumps(json_object),headers=headers)

RES = result.json()
print(RES)