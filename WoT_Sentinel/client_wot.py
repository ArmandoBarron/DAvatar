import requests as api #for APIs request
import json

data = {"username":"mariana_hiti","password":"*cinvestaV21*..."}
headers = {'Content-type': 'application/json'}
#url = "http://localhost:5001/login"
#url = "http://148.247.202.72:5055/login"
#url = "http://148.247.202.72:5001/login"
url = "http://148.247.202.72:5055/login"
result = api.post(url, data=json.dumps(data),headers=headers)
res = result.json()
token = res["token"]
print(token)
#token endpoint_service: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1NzM1fQ.dMXybOim1uU4pmaEfzYJsu4GYAOVB3gc4i5Epzcsyfs
#token endpoint_wot: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1Njg4fQ.cUfy4KHVWp4YlffT6bj0YpN0IJYMrFIw3b4uf1DtPGM
#http://localhost:5055/properties/sensors