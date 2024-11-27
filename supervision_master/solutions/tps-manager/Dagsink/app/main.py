from threading import Lock
from flask import Flask, request
from flask_api import status
from pymongo import MongoClient
import bson
from bson import ObjectId
from flask import jsonify
import json
from collections import namedtuple
from workflow import Workflow
import os
#from centinel_api import api_centinel as api
import logging #logger
import datetime

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.debug = True

MONGO_DB = os.environ['MONGO_DB']
#MONGO_DB = "localhost"
client = MongoClient(MONGO_DB,port=27017)
db = client.dagsink
workflows = {}
#centinel = api()
logging.basicConfig()
LOG = logging.getLogger('logger')

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

@app.route('/create', methods=['POST'])
def push_workflow():
    content = request.json
    print(content['host'])
    workflow = db.workflows.find_one({"name": content['name']})

    if workflow is not None: #if already exist
        deleteWF(workflow["_id"])
        wf = db.workflows.insert_one({'name':content['name'],
                                        'host' : content['host'],
                                        'tasks': content['tasks'],
                                        'creation_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return jsonify({"id": str(workflow["_id"])}), status.HTTP_201_CREATED
        #return jsonify({"id": str(workflow["_id"])}), status.HTTP_302_FOUND
    else: #create workflow
        wf = db.workflows.insert_one({'name':content['name'],
                                        'host' : content['host'],
                                        'tasks': content['tasks'],
                                        'creation_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        workflow = db.workflows.find_one({"name": content['name']})
        return jsonify({"id": str(workflow["_id"])}), status.HTTP_201_CREATED


@app.route("/getworkflow/<workflow_name>", methods=['GET'])
def getWorkflowByName(workflow_name):
    try:
        workflow = db.workflows.find_one({"name": workflow_name})
        return str(workflow["_id"])
    except bson.errors.InvalidId:
        return jsonify({"status": "error", "message": "Invalid name %s" % workflow_name}), status.HTTP_404_NOT_FOUND
    except TypeError:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % workflow_name}), status.HTTP_404_NOT_FOUND

@app.route("/<workflow_id>/<task>",methods=['GET'])
def getTask(workflow_id, task):
    try:
        workflow = db.workflows.find_one({"_id": ObjectId(workflow_id)})
        task = workflow['tasks'][task]
        return jsonify({"status": "ok", "task": task})
    except bson.errors.InvalidId as e:
        return jsonify({"status": "error", "message": "Invalid ID %s" % workflow_id}), status.HTTP_404_NOT_FOUND
    except TypeError:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % workflow_id}), status.HTTP_404_NOT_FOUND
    except KeyError as e:
        return jsonify({"status": "error", "message": "Task with key %s does not exist" % task})


@app.route("/<workflow_id>")
def getWorkflow(workflow_id):
    try:
        workflow = db.workflows.find_one({"_id": ObjectId(workflow_id)})
        return jsonify({"name": workflow['name'], "host": workflow['host'] ,"tasks": workflow['tasks'], "creation_at": workflow['creation_at'] })
    except bson.errors.InvalidId as e:
        return jsonify({"status": "error", "message": "Invalid ID %s" % workflow_id}), status.HTTP_404_NOT_FOUND
    except TypeError:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % workflow_id}), status.HTTP_404_NOT_FOUND



@app.route("/update/<workflow_id>/<task>/<parameter>", methods=['PUT'])
def update_task(workflow_id, task, parameter):
    try:
        value = request.args.get('value')
        workflow = db.workflows.find_one({"_id": ObjectId(workflow_id)})

        db.workflows.update({"_id": workflow['_id']},{'$set':{"tasks."+task+"."+parameter : value}}, True)

        #if parameter == 'working_dir':
        #    centinel.UpdateWorkingDir(workflow['name'],task,value )


    except bson.errors.InvalidId as e:
        return jsonify({"status": "error", "message": "Invalid ID %s" % workflow_id}), status.HTTP_404_NOT_FOUND
    except TypeError as e:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % workflow_id}), status.HTTP_404_NOT_FOUND
    except KeyError as e:
        return jsonify({"status": "error", "message": e}), status.HTTP_404_NOT_FOUND
    return jsonify({"status": "ok"})

# to receive notifications from a task
@app.route('/subscribe/<subscriber_id>/<to_id>/<task>')
def suscribe(subscriber_id, to_id, task):
    try:
        workflowSubscriber = db.workflows.find_one({"_id": ObjectId(subscriber_id)})
        workflowTarget = db.workflows.find_one({"_id": ObjectId(to_id)})  # only to check if the workflow exists
        targetObj = Workflow(workflowTarget["name"], workflowTarget["tasks"], creation_at=workflowTarget["creation_at"],
                             id=str(workflowTarget["_id"]))
        targetObj.addSubscriber(str(workflowSubscriber["_id"]))
        db.workflows.replace_one({"_id": workflowTarget['_id']}, targetObj.__dict__, True)  # update in the database
        # db.workflows.replace_one({"_id":targetObj.id}, targetObj.__dict__, True) #update in the database
        # workflowSubscriber
        return jsonify({"message": "ok"})
    except bson.errors.InvalidId as e:
        return jsonify({"status": "error", "message": "Invalid ID %s" % subscriber_id}), status.HTTP_404_NOT_FOUND
    except TypeError as e:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % subscriber_id}), status.HTTP_404_NOT_FOUND


@app.route('/list')
def list():
    cursor = db.workflows.find({})
    workflowsLst = []
    for workflow in cursor:
        workflowsLst.append({"id":str(workflow['_id']),  "name": workflow['name'],"host": workflow['host'], "tasks": workflow['tasks'], "creation_at": workflow['creation_at'] })
    return jsonify(workflowsLst)


@app.route('/check')
def check():
    return jsonify({"status": "ok"})

@app.route("/delete/<workflow_id>")
def deleteWF(workflow_id):
    try:
        query ={"_id":ObjectId(workflow_id)}
        db.workflows.delete_one(query)
        return jsonify({"status": "ok"})
    except bson.errors.InvalidId as e:
        return jsonify({"status": "error", "message": "Invalid ID %s" % workflow_id}), status.HTTP_404_NOT_FOUND
    except TypeError:
        return jsonify(
            {"status": "error", "message": "Workflow %s does not exist" % workflow_id}), status.HTTP_404_NOT_FOUND
    except KeyError as e:
        return jsonify({"status": "error", "message": "Workflow with key %s does not exist" % workflow_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9800,debug = True)
