#!/usr/bin/env python3.7
from flask import Flask
from flask import request, url_for
import json
import logging #logger
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
import pickle

from random import randint

import time

app = Flask(__name__)
LOGER = logging.getLogger()

models_folder= "./Models/"
try:
    if not os.path.exists(models_folder):
        os.makedirs(models_folder)
except FileExistsError:
    pass


@app.route('/')
def prueba():
    return "MLPNN Service"


@app.route('/mlprnn/training', methods=['POST'])
def MLPRNN_train():
    message = request.get_json()
    DF_data = message['data']
    params = message['params']

    list_var = params['list_var']
    test_size = params["test_size"]
    ToPredict = params["target"]
    if 'max_iter' in params: max_iter = params['max_iter'] 
    else: max_iter=500
    if 'solver' in params: solver = params['solver'] 
    else: solver="adam"
    if 'hidden_layer_sizes' in params: hidden_layer_sizes = tuple(params['hidden_layer_sizes']) 
    else: hidden_layer_sizes=(20,20)
    if 'model_tag' in params: model_tag = params['model_tag'] 
    else: model_tag="MLPR_NN_model_"+str(randint(1, 10000))

    DF_data = pd.DataFrame.from_records(DF_data) #pandas dataframe with all data

    #########################
    X = DF_data[list_var]
    y = DF_data[ToPredict]
    LOGER.error(DF_data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)


    #preprocessing
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    #TRAINING
    mlp = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,max_iter=max_iter,solver =  solver,verbose=True,alpha=.1)
    mlp.fit(X_train,y_train)

    #EVALUATION
    predictions = mlp.predict(X_test)
    score = metrics.r2_score(y_test, predictions)
    LOGER.error(score)

    pickle.dump(mlp, open(models_folder+model_tag, 'wb'))


    #figure
    #plt.figure(figsize=(10,10))     
    #sns.regplot(y_test, predictions, fit_reg=True, scatter_kws={"s": 100})
    #plt.ylabel("real values")
    #plt.title("Pollutant: "+ToPredict+" . R2 score:"+str(score))
    #plt.xlabel("regression values")
    #plt.show()



    return json.dumps({"status": "OK" , "result": {"model_tag":model_tag,"R2_score":score}})

@app.route('/mlprnn/predict', methods=['POST'])
def MLPRNN_predict():
    message = request.get_json()
    DF_data = message['data']
    params = message['params']

    if 'model_tag' in params: model_tag = params['model_tag'] 
    else: return json.dumps({"status": "ERROR" , "result": "BAD PARAMETERS"})
    if 'list_var' in params: list_var = params['list_var'] 
    else: return json.dumps({"status": "ERROR" , "result": "BAD PARAMETERS"})

    DF_data = pd.DataFrame.from_records(DF_data) #pandas dataframe with all data

    #########################
    X = DF_data[list_var]

    #preprocessing
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    #LOAD MODEL
    mlp = pickle.load(open(models_folder+model_tag, 'rb'))

    #RETURN PREDICTED DATA
    predictions = mlp.predict(X)
    DF_data['predictions'] = predictions

    return json.dumps({"status": "OK" , "result": json.loads(DF_data.to_json(orient='records'))})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug = True) 