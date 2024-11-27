import json
import numpy as np
import pandas as pd

def json2dataframe(data):
    arrData = []
    try:
        data=json.loads(data)
    except TypeError as s:
        pass


    for key,record in data.items():
        lista = []
        
        data_keys = record.keys()
        for k2,c in record.items():
            lista.append(c)
        arrData.append(lista)
    df = pd.DataFrame(np.array(arrData),columns=data_keys)
    data_keys= list(data_keys)
    #df[data_keys] = df[data_keys].apply(pd.to_numeric,errors='coerce') #tonumeric


    return df

def DF_Filter(df,filtter):
    filtter = filtter.split(",")
    return df[filtter]


