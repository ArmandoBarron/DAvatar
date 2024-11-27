from typing import ValuesView
from flask import Flask, jsonify, request, make_response
from functools import wraps
import json
import os
import data
import time
import jwt 
import hashlib
import datetime
import ast
import requests as api
import database.db_connector
app = Flask(__name__)
#LOCALHOST = "10.0.0.19"
LOCALHOST = os.getenv("LOCALHOST")
app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #data = request.get_json(force=True)
        #token = data["token"]
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        print(token)
        if not token:
            return jsonify({'error' : 'Token is missing!'}), 403
        try: 
            dt = jwt.decode(token,"secretkey")
        except Exception as e: 
            return jsonify({"error":str(e)})
        return f(*args, **kwargs)
    return decorated

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data["username"]
    password = data["password"]
    protectPass = hashlib.md5(password.encode())
    pp = protectPass.hexdigest()
    bdpass = database.db_connector.select_user_pass(username)
    if(pp == bdpass):
        token = jwt.encode({'user':username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=500)}, "secretkey")
        return jsonify({'token':token.decode('UTF-8')})
    return jsonify({"error":"Incorrect credentials"})

@app.route('/protected')
#@token_required
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/containers/container_<id_container>', methods=['GET'])
#@token_required
def container_tdscheme(id_container):
    if(len(id_container) == 12):
        td_schema = database.db_connector.select_container_tdSchema(id_container)
        td_schema = str(td_schema)
        return jsonify(td_schema)
    else:
        td_schema = database.db_connector.select_container_tdSchema_priv(id_container)
        td_schema = str(td_schema)
        return jsonify(td_schema)

@app.route('/containers/container_<id_container>/actions/<name_action>', methods=['POST','GET','PUT','DELETE'])
#@token_required
def container_action_post(id_container,name_action):
    if(len(id_container) == 12):
        data = ""
        uri_action = database.db_connector.select_action_uri(name_action)
        uri_action = str(uri_action[0])
        uri_action = uri_action.replace("localhost",LOCALHOST) 
        print(uri_action)
        print(LOCALHOST)
        try:
            data = request.get_json(force=True)
            content = request.content_type
            headers = {'Content-type': content}    
        except:
            try:
                data = request.values
                content = request.content_type
                print(content)
                headers = {'Content-type': content}   
            except:
                data = "Null"
        print("ID CONTAINER:" + str(id_container))
        td_schema_pub = json.loads(database.db_connector.select_container_tdSchema(id_container))
        # = json.loads(td_schema_pub)
        type_request = td_schema_pub["actions"][name_action]["forms"][0]["type"]
        name_cont = td_schema_pub["title"]
        """port = database.db_connector.select_container_port(id_container)
        uri_action = uri_action.replace("localhost",name_cont)
        uri_1 = uri_action.split(":")
        uri_2 = uri_1[2].split("/",1)

        uri_final = str(uri_1[0])+":"+str(uri_1[1])+":"+str(port)+"/"+str(uri_2[1])"""
        uri_final = uri_action+"?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDMzMDcwfQ.AZEWJyB4CqcquUcV4TpSRokmNo3qyGn-mdcgyDDAJXM"
        if(type_request == "POST" and data != "Null"):
            try:
                res = api.post(uri_final, data=json.dumps(data),headers=headers)
                result = res.json()
            except Exception as e: 
                result = {"error":str(e)}
        else:
            if(type_request == "GET" and data != "Null"):
                try:
                    res = api.get(uri_final, parameters=json.dumps(data),headers=headers)
                    result = res.json()
                except Exception as e: 
                    result = {"error":str(e)}
                
            else:
                if(type_request == "PUT" and data != "Null"):
                    try:
                        res = api.put(uri_final, data=json.dumps(data),headers=headers)
                        result = res.json()
                    except Exception as e: 
                        result = {"error":str(e)}
                else:
                    if(type_request == "DELETE" and data != "Null"):
                        try:
                            res = api.delete(uri_final, parameters=json.dumps(data),headers=headers)
                            result = res.json()
                        except Exception as e: 
                            result = {"error":str(e)}
        if(data == "Null"):
            result = {"message":"An error occurred while obtaining the data of the request"}

    return jsonify(result)

@app.route('/containers/container_<id_container>/extras/properties/<name_prop>', methods=['POST','GET','PUT','DELETE'])
#@token_required
def container_extras_properties(id_container,name_prop):
    if(len(id_container) == 12):
        uri_prop = database.db_connector.select_extra_uri(id_container,name_prop,"p")
        #uri_prop = str(uri_prop[0])
        print(uri_prop)
        uri_final = str(uri_prop)+"?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI2MDk1Njg4fQ.cUfy4KHVWp4YlffT6bj0YpN0IJYMrFIw3b4uf1DtPGM"
        print("URI FINAL:")
        print(uri_final)
        res = api.get(uri_final)
        result = res.json()
        """try:
            res = api.get(uri_final)
            result = res.json()
        except Exception as e: 
            result = {"error":str(e)}"""
    #return jsonify(uri_prop)
    #return uri_final
    return jsonify(result)


@app.route('/containers/container_<id_container>/extras/events/<name_eve>', methods=['POST','GET','PUT','DELETE'])
#@token_required
def container_extras_events(id_container,name_eve):
    if(len(id_container) == 12):
        uri_eve = database.db_connector.select_extra_uri(id_container,name_eve,"e")
        #uri_prop = str(uri_prop[0])
        print(uri_eve)
        uri_final = str(uri_eve)+"?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFyaWFuYV9oaXRpIiwiZXhwIjoxNjI5ODMxMDEyfQ.2aH3WZ07wF8v7FGfjfDxvdrBHBeeZh5ZL_KCp3pfkcE"
        print("URI FINAL:")
        print(uri_final)
        res = api.get(uri_final)
        result = res.json()
        """try:
            res = api.get(uri_final)
            result = res.json()
        except Exception as e: 
            result = {"error":str(e)}"""
    #return jsonify(uri_prop)
    #return uri_final
    return jsonify(result)

@app.route('/containers/container_<id_container>/<value>', methods=['GET'])
#@token_required
def container_info(id_container,value):
    if(len(id_container) == 12):
        name,status,image,volumes,entrypoint,platform,description,image_p,volumes_p,status_p,c_util,m_util,n_util,f_util,c_lvl,m_lvl,n_lvl,f_lvl,time,utility_p = database.db_connector.select_container_info(id_container)
        if(image_p == 0):
            image = "private"
        if(volumes_p == 0):
            volumes = "private"
            entrypoint = "private"
        if(status_p == 0):
            status = "private"
        if(utility_p == 0):
            c_util = "private"
            m_util = "private"
            n_util = "private"
            f_util = "private"
            time = "private"
        if(value == "info"):
            info = {"name":name,"status":status,"image":image,"volumes":volumes,"entrypoint":entrypoint,"platform":platform,"description":description,"fu":{"cpu_utilization":c_util,"memory_utilization":m_util,"network_utilization":n_util,"fileSystem_utilization":f_util,"timestamp":time}}
            return jsonify(info)
        if(value == "name"):
            r = {"name":name}
            return jsonify(r)
        if(value == "status"):
            r = {"status":status}
            return jsonify(r)
        if(value == "image"):
            r = {"image":image}
            return jsonify(r)
        if(value == "volumes"):
            r = {"volumes":volumes}
            return jsonify(r)
        if(value == "entrypoint"):
            r = {"entrypoint":entrypoint}
            return jsonify(r)
        if(value == "platform"):
            r = {"platform":platform}
            return jsonify(r)
        if(value == "description"):
            r = {"description":description}
            return jsonify(r)
        if(value == "cpu_utilization"):
            r = {"cpu_utilization":c_util}
            return jsonify(r)
        if(value == "memory_utilization"):
            r = {"memory_utilization":m_util}
            return jsonify(r)
        if(value == "network_utilization"):
            r = {"network_utilization":n_util}
            return jsonify(r)
        if(value == "fileSystem_utilization"):
            r = {"fileSystem_utilization":f_util}
            return jsonify(r)
        if(value == "cpu_utilization_high"):
            if(utility_p == 1):
                if(c_lvl == 3):
                    r = {"cpu_utilization_high":"True"}
                    return jsonify(r)
                else:
                    r = {"cpu_utilization_high":"False"}
                    return jsonify(r)
            else:
                r = {"cpu_utilization_high":"private"}
                return jsonify(r)
        if(value == "cpu_utilization_medium"):
            if(utility_p == 1):
                if(c_lvl == 2):
                    r = {"cpu_utilization_medium":"True"}
                    return jsonify(r)
                else:
                    r = {"cpu_utilization_medium":"False"}
                    return jsonify(r)
            else:
                r = {"cpu_utilization_medium":"private"}
                return jsonify(r)
        if(value == "cpu_utilization_low"):
            if(utility_p == 1):
                if(c_lvl == 1):
                    r = {"cpu_utilization_low":"True"}
                    return jsonify(r)
                else:
                    r = {"cpu_utilization_low":"False"}
                    return jsonify(r)
            else:
                r = {"cpu_utilization_low":"private"}
                return jsonify(r)
        if(value == "memory_utilization_high"):
            if(utility_p == 1):
                if(m_lvl == 3):
                    r = {"memory_utilization_high":"True"}
                    return jsonify(r)
                else:
                    r = {"memory_utilization_high":"False"}
                    return jsonify(r)
            else:
                r = {"memory_utilization_high":"private"}
                return jsonify(r)
        if(value == "memory_utilization_medium"):
            if(utility_p == 1):
                if(m_lvl == 2):
                    r = {"memory_utilization_medium":"True"}
                    return jsonify(r)
                else:
                    r = {"memory_utilization_medium":"False"}
                    return jsonify(r)
            else:
                r = {"memory_utilization_medium":"private"}
                return jsonify(r)
        if(value == "memory_utilization_low"):
            if(utility_p == 1):
                if(m_lvl == 1):
                    r = {"memory_utilization_low":"True"}
                    return jsonify(r)
                else:
                    r = {"memory_utilization_low":"False"}
                    return jsonify(r)
            else:
                r = {"memory_utilization_low":"private"}
                return jsonify(r)
        if(value == "network_utilization_high"):
            if(utility_p == 1):
                if(n_lvl == 3):
                    r = {"network_utilization_high":"True"}
                    return jsonify(r)
                else:
                    r = {"network_utilization_high":"False"}
                    return jsonify(r)
            else:
                r = {"network_utilization_high":"private"}
                return jsonify(r)
        if(value == "network_utilization_medium"):
            if(utility_p == 1):
                if(n_lvl == 2):
                    r = {"network_utilization_medium":"True"}
                    return jsonify(r)
                else:
                    r = {"network_utilization_medium":"False"}
                    return jsonify(r)
            else:
                r = {"network_utilization_medium":"private"}
                return jsonify(r)
        if(value == "network_utilization_low"):
            if(utility_p == 1):
                if(n_lvl == 1):
                    r = {"network_utilization_low":"True"}
                    return jsonify(r)
                else:
                    r = {"network_utilization_low":"False"}
                    return jsonify(r)
            else:
                r = {"network_utilization_low":"private"}
                return jsonify(r)
        if(value == "fileSystem_utilization_high"):
            if(utility_p == 1):
                if(f_lvl == 3):
                    r = {"fileSystem_utilization_high":"True"}
                    return jsonify(r)
                else:
                    r = {"fileSystem_utilization_high":"False"}
                    return jsonify(r)
            else:
                r = {"fileSystem_utilization_high":"private"}
                return jsonify(r)
        if(value == "fileSystem_utilization_medium"):
            if(utility_p == 1):
                if(f_lvl == 2):
                    r = {"fileSystem_utilization_medium":"True"}
                    return jsonify(r)
                else:
                    r = {"fileSystem_utilization_medium":"False"}
                    return jsonify(r)
            else:
                r = {"fileSystem_utilization_medium":"private"}
                return jsonify(r)
        if(value == "fileSystem_utilization_low"):
            if(utility_p == 1):
                if(f_lvl == 1):
                    r = {"fileSystem_utilization_low":"True"}
                    return jsonify(r)
                else:
                    r = {"fileSystem_utilization_low":"False"}
                    return jsonify(r)
            else:
                r = {"fileSystem_utilization_low":"private"}
                return jsonify(r)

        if(value == "receivesfrom"):
            app = database.db_connector.select_container_app(id_container)
            structure = database.db_connector.select_app_structure(app)
            name_cont = database.db_connector.select_container_name(id_container)
            structure = ast.literal_eval(structure)
            edges = structure["data"]["edges"]
            receivesfrom = []
            for i in range(0,len(edges)):
                if(edges[i][1] == name_cont):
                    receivesfrom.append(edges[i])
            receivesfrom_json = {"receives_from":{}}
            receivesfrom_json["receives_from"] = receivesfrom
            return jsonify(receivesfrom_json)
        if(value == "sendto"):
            app = database.db_connector.select_container_app(id_container)
            structure = database.db_connector.select_app_structure(app)
            name_cont = database.db_connector.select_container_name(id_container)
            structure = ast.literal_eval(structure)
            edges = structure["data"]["edges"]
            sendto = []
            for i in range(0,len(edges)):
                if(edges[i][0] == name_cont):
                    sendto.append(edges[i])
            sendto_json = {"send_to":{}}
            sendto_json["send_to"] = sendto
            return jsonify(sendto_json)

    else:
        name,status,image,volumes,entrypoint,platform,description,c_util,m_util,n_util,f_util,c_lvl,m_lvl,n_lvl,f_lvl,time = database.db_connector.select_container_info_priv(id_container)
        if(value == "info"):
            info = {"name":name,"status":status,"image":image,"volumes":volumes,"entrypoint":entrypoint,"platform":platform,"description":description,"fu":{"cpu_utilization":c_util,"memory_utilization":m_util,"network_utilization":n_util,"fileSystem_utilization":f_util,"timestamp":time}}
            return jsonify(info)
        if(value == "name"):
            r = {"name":name}
            return jsonify(r)
        if(value == "status"):
            r = {"status":status}
            return jsonify(r)
        if(value == "image"):
            r = {"image":image}
            return jsonify(r)
        if(value == "volumes"):
            r = {"volumes":volumes}
            return jsonify(r)
        if(value == "entrypoint"):
            r = {"entrypoint":entrypoint}
            return jsonify(r)
        if(value == "platform"):
            r = {"platform":platform}
            return jsonify(r)
        if(value == "description"):
            r = {"description":description}
            return jsonify(r)
        if(value == "cpu_utilization"):
            r = {"cpu_utilization":c_util}
            return jsonify(r)
        if(value == "memory_utilization"):
            r = {"memory_utilization":m_util}
            return jsonify(r)
        if(value == "network_utilization"):
            r = {"network_utilization":n_util}
            return jsonify(r)
        if(value == "fileSystem_utilization"):
            r = {"fileSystem_utilization":f_util}
            return jsonify(r)
        #cambiar, por prueba no se cambio
        if(value == "cpu_utilization_high"):
            if(c_lvl == 3):
                return("True")
            else:
                return("False")
        if(value == "cpu_utilization_medium"):
            if(c_lvl == 2):
                return("True")
            else:
                return("False")
        if(value == "cpu_utilization_low"):
            if(c_lvl == 1):
                return("True")
            else:
                return("False")
        if(value == "memory_utilization_high"):
            if(m_lvl == 3):
                return("True")
            else:
                return("False")
        if(value == "memory_utilization_medium"):
            if(m_lvl == 2):
                return("True")
            else:
                return("False")
        if(value == "memory_utilization_low"):
            if(m_lvl == 1):
                return("True")
            else:
                return("False")
        if(value == "network_utilization_high"):
            if(n_lvl == 3):
                return("True")
            else:
                return("False")
        if(value == "network_utilization_medium"):
            if(n_lvl == 2):
                return("True")
            else:
                return("False")
        if(value == "network_utilization_low"):
            if(n_lvl == 1):
                return("True")
            else:
                return("False")
        if(value == "fileSystem_utilization_high"):
            if(f_lvl == 3):
                return("True")
            else:
                return("False")
        if(value == "fileSystem_utilization_medium"):
            if(f_lvl == 2):
                return("True")
            else:
                return("False")
        if(value == "fileSystem_utilization_low"):
            if(f_lvl == 1):
                return("True")
            else:
                return("False")

@app.route('/applications/app_<name>', methods=['GET'])
#@token_required
def application_tdscheme(name):
    td_schema = database.db_connector.select_app_tdSchema(name)
    return jsonify(td_schema)

@app.route('/applications/app_<name>/info', methods=['GET'])
#@token_required
def application_info(name):
    containers,desc = database.db_connector.select_app_info(name)
    info = {"name":name,"description":desc,"containers":{}}
    for i in range(0,len(containers)):
        info["containers"][str(i+1)] = containers[i]
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
