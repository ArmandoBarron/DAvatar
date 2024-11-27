#!/usr/bin/env python3.7
from flask import Flask
from flask import request, url_for
import json
from Functions import *

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics

import matplotlib.pyplot as plt

import numpy as np
import time

app = Flask(__name__)
GRAPHS_PATH = "./static"


def apply_labels(data,labeled_data,idx):
    c = len(data.index)
    data["class"] = [*range(c)]

    for index,row in labeled_data.iterrows():
        data.loc[data[idx] == row[idx], 'class'] = row['class']
    
    print(data)
    return data

def NAN_format(df):
    df.replace('None', np.nan, inplace=True)
    df.replace('NA', np.nan, inplace=True)
    df.replace('Na', np.nan, inplace=True)
    df.replace('Null', np.nan, inplace=True)
    return df


def preproc(data,columns,idx=None):
    dataframe = json2dataframe(data)
    F_dataframe = dataframe
    #data filter 
    if idx is not None:
        numeric_columns = columns
        columns = idx+","+columns
    if columns != "all":
        F_dataframe = DF_Filter(dataframe,columns)
        if idx is not None:
            F_dataframe = NAN_format(F_dataframe)
            F_dataframe = F_dataframe.fillna(F_dataframe.mean())
            F_dataframe[numeric_columns.split(",")] = F_dataframe[numeric_columns.split(",")].astype(str).astype(float)
            F_dataframe=F_dataframe.groupby(idx).mean().reset_index()
        else:
            F_dataframe = NAN_format(F_dataframe)
            F_dataframe = F_dataframe.fillna(F_dataframe.mean())
            F_dataframe[columns.split(",")] = F_dataframe[columns.split(",")].astype(str).astype(float)



    #fill na values
    F_dataframe = F_dataframe.fillna(F_dataframe.mean())

    return F_dataframe,dataframe

@app.route('/')
def prueba():
    return "Clustering Service"

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@app.route('/clustering/kmeans', methods=['POST'])
def kmeans(K=2, columns="all"):
    #get data
    message = request.get_json()
    data = message['data']
    if 'K' in message: K = message['K']
    if 'columns' in message: columns = message['columns']
    if 'index' in message: idx = message['index'] #filter by index (mean)
    else: idx=None
    F_dataframe,dataframe = preproc(data,columns,idx=idx)

    #algorithm k means
    try:
        kmeans = KMeans(n_clusters=K, random_state=0).fit(DF_Filter(F_dataframe,columns))
    except ValueError as v:
        return {"status": "ERROR" ,"result": dataframe.to_json(orient='records')}

    #add labels
    if idx is not None:
        F_dataframe['class']=kmeans.labels_
        dataframe= apply_labels(dataframe,F_dataframe,idx)
    else:
        dataframe["class"] = kmeans.labels_
    return json.dumps({"status": "OK" ,"path":None, "result": json.loads(dataframe.to_json(orient='records'))})


@app.route('/clustering/herarhical', methods=['POST'])
def herarh(K=2, columns="all"):
    #get data
    message = request.get_json()
    data = message['data']
    if 'K' in message: K = message['K']
    if 'columns' in message: columns = message['columns']
    if 'index' in message: idx = message['index'] #filter by index (mean)
    else: idx=None

    F_dataframe,dataframe = preproc(data,columns,idx=idx)

    #algorithm herarhical
    try:
        ward = AgglomerativeClustering(n_clusters=K, linkage='single').fit(DF_Filter(F_dataframe,columns))
    except ValueError as v:
        return {"status": "ERROR" ,"result": dataframe.to_json(orient='records')}

    if idx is not None:
        F_dataframe['class']=ward.labels_
        dataframe= apply_labels(dataframe,F_dataframe,idx)
    else:
        dataframe["class"] = ward.labels_
    return json.dumps({"status": "OK" ,"path":None, "result": json.loads(dataframe.to_json(orient='records'))})


@app.route('/clustering/silhouette', methods=['POST'])
def silhouette():
    #get data
    message = request.get_json()
    data = message['data']
    if 'columns' in message: columns = message['columns']
    if 'index' in message: idx = message['index'] #filter by index (mean)
    else: idx=None

    F_dataframe,dataframe = preproc(data,columns,idx=idx)

    km_results = []
    her_results = []

    labels_results = []
    maxK = 2

    for k in range(2,15):
        try:
            #KMEANS
            kmeans = KMeans( n_clusters=k )
            kmeans.fit(DF_Filter(F_dataframe,columns))
            pl_kmeans = kmeans.labels_
            #HER
            ward = AgglomerativeClustering(n_clusters=k, linkage='single').fit(DF_Filter(F_dataframe,columns))
            pl_her = ward.labels_

            kmeans_sil = metrics.silhouette_score(DF_Filter(F_dataframe,columns), pl_kmeans , metric='euclidean')
            her_sil = metrics.silhouette_score(DF_Filter(F_dataframe,columns), pl_her , metric='euclidean')

        except ValueError as v:
            break
        #print( "Silhouette Score (K-Means, %d clusters) (her, %d clusters) =" % (k,k), kmeans_sil, her_sil)


        km_results.append( kmeans_sil )
        her_results.append(her_sil)
        labels_results.append([pl_kmeans,pl_her])

        maxK = maxK+1


    #maximum result
    M_km = km_results.index(max(km_results))
    M_hr = her_results.index(max(her_results))

    winner = [max(km_results),max(her_results)]
    winner = winner.index(max(winner))
    
    if winner == 0: #km wins
        w_lab =  labels_results[M_km][winner]
        win = "BEST: KMEANS - %s Clusters " % (int(M_km)+2)
    if winner == 1: #hr wins
        w_lab =  labels_results[M_km][winner]
        win = "BEST: HIERARCHICAL  %s Clusters" %(int(M_hr)+2)

# PLOT ---------------
    picture_name= time.strftime("%c")
    picture_name = hash(str(picture_name)+str(k)+str(winner))
    fig, ax = plt.subplots()
    plt.title(win)
    ax.plot( [i for i in range(2,maxK)], km_results )
    ax.plot( [i for i in range(2,maxK)], her_results )
    
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('Silhouette Score')
    plt.xticks([i for i in range(2,maxK)])
    #plt.show()
    PATH = "%s/%s.png" %(GRAPHS_PATH,picture_name)
    plt.savefig(PATH)
    plt.close()
#---------------------

    if idx is not None:
        F_dataframe['class']= w_lab
        dataframe= apply_labels(dataframe,F_dataframe,idx)
    else:
        dataframe["class"] =  w_lab
    
    return json.dumps({"status": "OK" ,"path":PATH[1:] ,"result": json.loads(dataframe.to_json(orient='records'))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug = True) 