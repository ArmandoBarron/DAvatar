#!/usr/bin/env python3.7
from flask import Flask
from flask import request, url_for
from bins import *
import json

app = Flask(__name__)

@app.route('/')
def prueba():
    return "Meteorological microservice"

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@app.route('/GetEmas', methods=['POST'])
def byHour():
    try:
        puntos = request.get_json()
        result = GetEmasByDate(puntos['polygon'],puntos['inicio'],puntos['fin'],puntos['hora'])
        stations =[]
        i=0
        for estacion in result:
            i=i+1
            data = {i:{ \
                'Antena':estacion[0],\
                'Fecha':estacion[1],
                'Latitud':estacion[2],\
                'Longitud':estacion[3],\
                'Temperatura':estacion[5],\
                'Humedad':estacion[6], \
                'PresionBarometrica':estacion[7], \
                'Precipitacion':estacion[8], \
                'RadiacionSolar':estacion[9], \
                }}
            stations.append(data)
        return json.dumps(stations)
    except Exception as e:
        return "BAD REQUEST " +str(e)

@app.route('/GetEmas60', methods=['POST'])
def by60min():
    try:
        puntos = request.get_json()
        result = GetEmasByDate(puntos['polygon'],puntos['inicio'],puntos['fin'],"60")
        stations =[]
        i=0
        for estacion in result:
            i=i+1
            data = {i:{ \
                'Antena':estacion[0],\
                'Fecha':estacion[1],
                'Latitud':estacion[2],\
                'Longitud':estacion[3],\
                'Temperatura':estacion[5],\
                'Humedad':estacion[6], \
                'PresionBarometrica':estacion[7], \
                'Precipitacion':estacion[8], \
                'RadiacionSolar':estacion[9], \
                }}
            stations.append(data)
        return json.dumps(stations)
    except Exception as e:
        return "BAD REQUEST " +str(e)


@app.route('/GetMerra', methods=['POST'])
def byMerra():
    try:
        puntos = request.get_json()
        result = GetMerraByDate(puntos['polygon'],puntos['inicio'],puntos['fin'])
        stations =[]
        i=0
        for estacion in result:
            i=i+1
            data = {i:{ \
                'Antena':estacion[0],\
                'Fecha':estacion[1],\
                'Latitud':estacion[2],\
                'Longitud':estacion[3],\
                'Temp_ max':estacion[4],\
                'Temp_min':estacion[5], \
                'Temp_mean':estacion[6]
                }}
            stations.append(data)

        #for estacion in emas:
        #   print estacion[0],estacion[3]
        return json.dumps(stations)
    except Exception as e:
        return "BAD REQUEST " +str(e)



@app.route('/Histo-MERRA', methods=['POST'])
def HistoricoMerra():
    try:
        puntos = request.get_json()
        result = GetMerraByDate(puntos['polygon'],1980,2011,hora="year")
        stations =[]
        for estacion in result:
            data = { \
                'Antena':estacion[0],\
                'Fecha':estacion[1],\
                'Latitud':estacion[2],\
                'Longitud':estacion[3],\
                'Temp_max':estacion[4],\
                'Temp_min':estacion[5], \
                'Temp_mean':estacion[6]
                }
            stations.append(data)

        return json.dumps(stations)
    except Exception as e:
        return "BAD REQUEST " +str(e)

@app.route('/GetbyRange', methods=['POST'])
def byRange():
    try:
        puntos = request.get_json()
        result = GetByRange(puntos['polygon'],puntos['inicio'],puntos['fin'])
        stations =[]
        i=0
        for estacion in result:
            i=i+1
            data = {i:{ \
                'Antena':estacion[0],\
                'Fecha':estacion[1],\
                'Latitud':estacion[2],\
                'Longitud':estacion[3],\
                'Estado':estacion[4],\
                'Temp_max_emas':estacion[5],\
                'Temp_min_emas':estacion[6],\
                'Temp_max_merra':estacion[7], \
                'Temp_min_merra':estacion[8], \
                'Differential_max':estacion[9], \
                'Differential_min':estacion[10] 
                }}
            stations.append(data)
        return json.dumps(stations)
    except Exception as e:
        return "BAD REQUEST " +str(e)

# IMAGENES DE LA SILUETA
@app.route('/ClustImages', methods=['POST'])
def ClustImg():
    try:
        puntos = request.get_json()
        if 'fill' not in puntos:
            llenar = False
        else:
            llenar = str2bool(puntos['fill'])

        variables = puntos['variables'].split(",")
        fuentes = puntos['fuentes'].split(",")
        if(len(fuentes)==1):
            variables = format_variables(variables,fuentes[0])
            result = GetSilhouette(puntos['polygon'],puntos['inicio'],puntos['fin'],int(puntos['K']),llenar,fuentes[0],"NA",variables,onlyone=True)
        else: 
            variables = format_variables(variables,"DIFERENCIAL")
            result = GetSilhouette(puntos['polygon'],puntos['inicio'],puntos['fin'],int(puntos['K']),llenar,fuentes[0],fuentes[1],variables)
        return json.dumps(result)
    except Exception as e:
        return "BAD REQUEST " +str(e)


@app.route('/Clustering', methods=['POST'])
def byClust():

    puntos = request.get_json()
    if 'type' not in puntos:
        tipo = 1
    else:
        tipo=int(puntos['type'])
    if 'fill' not in puntos:
        llenar = False
    else:
        llenar = str2bool(puntos['fill'])
    if 'group' not in puntos:
        group = None
    else:
        group = str2bool(puntos['group'])


    variables = puntos['variables'].split(",")
    fuentes = puntos['fuentes'].split(",")
    sources =[]; stations =[]
    #obtener los datos de las fuentes
    for fuente in fuentes:
        sources.append(GetSource(puntos['polygon'],puntos['inicio'],puntos['fin'],fuente))

    if (len(fuentes)==1):
        variables = format_variables(variables,fuentes[0])
        if fuentes[0]=="EMASMAX":
                extraData = GetEmasByDate(puntos['polygon'],puntos['inicio'],puntos['fin'],'24')
                sources[0] = joindata(sources[0],extraData,[[1,1],[4,4]],[5,6,7,8,9] )
        result,images = Clustering(sources[0],int(puntos['K']),False,tipo,variables=variables,group=group)
        if fuentes[0]=="EMASMAX":
            i=0
            for estacion in result:
                i+=1
                data = {i:{ \
                    'Antena':estacion['0'],\
                    'Fecha':estacion['1'],\
                    'Latitud':estacion['2'],\
                    'Longitud':estacion['3'],\
                    'Codigo':estacion['4'],\
                    'Temp_max':estacion['5'],\
                    'Temp_min':estacion['6'],\
                    'Temp_mean':estacion['7'],\
                    'Humedad':estacion['8'],\
                    'Presion_barometrica':estacion['9'],\
                    'Precipitacion':estacion['10'],\
                    'Radiacion_solar':estacion['11'], \
                    'Etiqueta_clase':estacion['class']\
                    }}

                stations.append(data)             

        if fuentes[0]=="MERRA":
            i=0
            for estacion in result:
                i+=1
                data = {i:{ \
                    'Antena':estacion['0'],\
                    'Fecha':estacion['1'],\
                    'Latitud':estacion['2'],\
                    'Longitud':estacion['3'],\
                    'Codigo':estacion['0'],\
                    'Temp_max':estacion['4'],\
                    'Temp_min':estacion['5'],\
                    'Temp_mean':estacion['6'],\
                    'Etiqueta_clase':estacion['class']\
                    }}

                stations.append(data)

    if (len(fuentes)==2):
        variables = format_variables(variables,"DIFERENCIAL")
        result = GetDiff(puntos['polygon'],puntos['inicio'],puntos['fin'],tipo,llenar,sources[0],sources[1]) 
        extraData = GetEmasByDate(puntos['polygon'],puntos['inicio'],puntos['fin'],'24')
        result = joindata(result,extraData,[[1,1],[4,4]],[5,6,7,8,9] )
        result,images = Clustering(result,int(puntos['K']),False,tipo,variables=variables,group=group)
        
        #return json.dumps(result)
        #result = GetClusters(puntos['polygon'],puntos['inicio'],puntos['fin'],int(puntos['K']),int(puntos['type']))

        i=0
        for estacion in result:
            i+=1
            data = {i:{ \
                'Antena':estacion['0'],\
                'Fecha':estacion['1'],\
                'Latitud':estacion['2'],\
                'Longitud':estacion['3'],\
                'Codigo':estacion['4'],\
                'Temp_max_emas':estacion['5'],\
                'Temp_min_emas':estacion['6'],\
                'Temp_max_merra':estacion['7'], \
                'Temp_min_merra':estacion['8'], \
                'Differential_max':estacion['9'], \
                'Differential_min':estacion['10'],\
                'Temp_mean_merra':estacion['11'], \
                'Temp_mean_emas':estacion['12'],\
                'Humedad':estacion['13'],\
                'Presion_barometrica':estacion['14'],\
                'Precipitacion':estacion['15'],\
                'Radiacion_solar':estacion['16'], \
                'Etiqueta_clase':estacion['class']\
                }}

            stations.append(data)

    json_response = {"results":stations,"images":images}
    return json.dumps(json_response)

@app.route('/GraphDates', methods=['POST'])
def GraphsDates():
    try:
        puntos = request.get_json()
        img = GetGraphDates(puntos['polygon'],puntos['inicio'],puntos['fin'])
        i=0
        dates =[]
        for im in img:
            i=i+1
            data = {i:im}
            dates.append(data)
        return json.dumps(dates)
    except Exception as e:
        return "BAD REQUEST " +str(e)

@app.route('/GraphStations', methods=['POST'])
def GraphsStat():
    try:
        puntos = request.get_json()
        stat = GetGraphStations(puntos['polygon'],puntos['inicio'],puntos['fin'])
        i=0
        dates =[]
        for As in stat:
            data = {As[0]:As[1]}
            dates.append(data)
        return json.dumps(dates)
    except Exception as e:
        return "BAD REQUEST " +str(e)


@app.route('/summary', methods=['POST'])
def summary():
    try:
        data = request.get_json()
        polygon = data['polygon']
        inicio = data['inicio']
        fin = data['fin']
        result = Summary(polygon, inicio, fin)
        return json.dumps(result)
    except Exception as e:
        return "BAD REQUEST " +str(e)


@app.route('/summary-aas', methods=['POST'])
def summaryAAS():
    try:
        data = request.get_json()
        datos= data['data']
        parametros = data['params']

        result = Summary_service(datos, parametros)
        return json.dumps(result)
    except Exception as e:
        return "BAD REQUEST " +str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200,debug = True)
    #ssl_context=('Certificados/cert.pem', 'Certificados/key.pem')