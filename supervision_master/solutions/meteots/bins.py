from HandlerDB import *
import csv
from os.path import join,isfile
from os import mkdir,path,system,walk
import random
import subprocess
import requests
import configparser
from time import sleep
import shutil
import json
import numpy as np 
import pandas as pd
import threading
import urllib.request


#import commands

base = "./"
fout= "static/" #/volumen
#fout = "volumen/"

MAX_DIR = 300
config = configparser.ConfigParser()
config.read('config.ini')
IPHost=config['Services']['ip']
C_port=config['Services']['ClustPort']
S_port=config['Services']['SummaryPort']
#CI_port=config['Services']['CImgPort']
GS_port=config['Services']['GStatPort']
GD_port=config['Services']['GDatePort']

CLUST_WORKERS = C_port.split(",")
C_WORKERS_NUM = len(CLUST_WORKERS)
C_GLOBAL_RESULTS = dict()
C_GLOBAL_IMAGES = dict()

def GetSource(puntos,inicio,fin,source,hora = "60"):
	conexion = HandlerDB()
	poly = format_polygon(puntos)
	DS = conexion.GetByFont(poly,inicio,fin,hora,source) #EMASMAX
	conexion.CerrarConexion()
	return DS

def GetByRange(puntos,inicio,fin):
	conexion = HandlerDB()
	poly ="("
	for i in range(1,len(puntos)+1):
		poly = poly+"("+str(puntos[str(i)]['lon'])+","+str(puntos[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 
	stations = conexion.GetInsideDateRange(poly,inicio,fin)
	conexion.CerrarConexion()
	return stations

def GetEmasByDate(puntos,inicio,fin,hora):
	conexion = HandlerDB()
	poly ="("
	for i in range(1,len(puntos)+1):
		poly = poly+"("+str(puntos[str(i)]['lon'])+","+str(puntos[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 
	result = conexion.GetByFont(poly,inicio,fin,hora,"EMAS")
	conexion.CerrarConexion()
	return result

def GetMerraByDate(puntos,inicio,fin,hora = ""):
	conexion = HandlerDB()
	poly ="("
	for i in range(1,len(puntos)+1):
		poly = poly+"("+str(puntos[str(i)]['lon'])+","+str(puntos[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 
	result = conexion.GetByFont(poly,inicio,fin,hora,"MERRA")
	conexion.CerrarConexion()
	return result

# DIFERENCIAL ENTRE 2 FUENTES
def GetDiff(puntos,inicio,fin,tipo,fill,DS1,DS2):
	conexion = HandlerDB()
	poly ="("
	for i in range(1,len(puntos)+1):
		poly = poly+"("+str(puntos[str(i)]['lon'])+","+str(puntos[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 

	#DS1 = conexion.GetByFont(poly,inicio,fin,"60",source1) #EMASMAX
	#DS2 = conexion.GetByFont(poly,inicio,fin,"60",source2) ##MERRA

	stations = Transversal(DS2,DS1,[[1,1],[0,4]],[[4,5],[5,6]],option=fill)
	conexion.CerrarConexion()
	if len(stations) <1:
		return stations
	return stations

def GetClusters(puntos,inicio,fin,k,tipo):
	conexion = HandlerDB()
	poly ="("
	for i in range(1,len(puntos)+1):
		poly = poly+"("+str(puntos[str(i)]['lon'])+","+str(puntos[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 

	stations = conexion.GetInsideDateRange(poly,inicio,fin)
	conexion.CerrarConexion()
	if len(stations) <1:
		return stations
	result,images = Clustering(stations,k,False,tipo) 
	return result

def Clustering(diff,k,images,tipo,variables = "10,11",group=None):
	directory=str(random.randint(0,MAX_DIR))
	if not path.exists(base+fout):
		mkdir(base+fout)
	if not path.exists(base+fout+"clust"):
		mkdir(base+fout+"clust")
	if not path.exists(base+fout+"clust/"+directory):
		mkdir(base+fout+"clust/"+directory)
	else:
		shutil.rmtree(base+fout+"clust/"+directory, ignore_errors=True)
		mkdir(base+fout+"clust/"+directory)
	
	df = pd.DataFrame(diff)
	if group is not None:
		groupers = df[int(group)].unique().tolist() #agrupation 
		data = dict()
		for g in groupers:
			temp = df.loc[df[int(group)] == g]
			size= len(temp.index)
			if size>k:
				data[g]=df.loc[df[int(group)] == g]
	else:
		dataset= df.to_json(orient='index')
	# ejecutar R
	if(k==0):
		tipo = 0
	
	if tipo==0: algh = "silhouette"
	elif tipo ==1: algh = "kmeans"
	elif tipo == 2: algh=  "herarhical"

	data_results = []
	images_path = []
	if group is None:
		worker = RandomChoice(CLUST_WORKERS)
		url = 'http://%s/clustering/%s' %(worker,algh)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		Tosend = {"K":k,"data":dataset,"columns":variables,"index":"0"}
		result = requests.post(url, data=json.dumps(Tosend),headers=headers)
		RES = result.json()
		if RES['status']=="OK":
			data_results = RES['result']
			if RES['path'] is not None:
				images_path = {"path":RES['path'], "date": "range" } 
				url_image = 'http://%s%s'  %(worker,RES['path']) #download image
				urllib.request.urlretrieve(url_image, "./static/"+RES['path'].split("/")[2] )
	else: #clustreing for each day
		workload_worker=dict()
		glist = dict()
		for x in CLUST_WORKERS:
			workload_worker[x]=[]
		for g in groupers:
			try:
				dataset = data[g]
				worker = TwoChoises(workload_worker)
				dataset = dataset.to_json(orient='index')
				workload_worker[worker].append({"data":dataset,"group":g} )
			except KeyError as KE:
				pass


		global C_GLOBAL_RESULTS,C_GLOBAL_IMAGES
		idr= str(random.randint(0,100000))
		C_GLOBAL_RESULTS[idr]=[]
		C_GLOBAL_IMAGES[idr]=[]#dataresults
		T = []
		for x in CLUST_WORKERS: #create threads
			T.append(threading.Thread(target=clustering_worker_func, args=(x,workload_worker[x],k,algh,variables,idr)))

		for x in T:
			x.start()
		for x in T:
			x.join()
		data_results= C_GLOBAL_RESULTS[idr]
		images_path = C_GLOBAL_IMAGES[idr]
		del C_GLOBAL_RESULTS[idr]
		del C_GLOBAL_IMAGES[idr]

			
	return data_results,images_path

# ------------------------Silhouette
def clustering_worker_func(worker,workload,k,algh,variables,idr):
	global C_GLOBAL_RESULTS,C_GLOBAL_IMAGES
	for dataset in workload:
		g = dataset["group"]
		dataset = dataset["data"]
		url = 'http://%s/clustering/%s' %(worker,algh)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		Tosend = {"K":k,"data":dataset,"columns":variables}
		result = requests.post(url, data=json.dumps(Tosend),headers=headers)
		RES = result.json()
		if RES['status']=="OK":
			if RES['path'] is not None:
				jsonString = {"path":RES['path'], "date": g } 
				C_GLOBAL_IMAGES[idr].append(jsonString)
				url_image = 'http://%s%s'  %(worker,RES['path'])
				urllib.request.urlretrieve(url_image,  "./static/"+RES['path'].split("/")[2] )

			for x in RES['result']:
				C_GLOBAL_RESULTS[idr].append(x)

def GetSilhouette(puntos,inicio,fin,k,fill,source1,source2,vari,onlyone=False):
	conexion = HandlerDB()
	poly =format_polygon(puntos)
	if(onlyone==False):
		DS1 = conexion.GetByFont(poly,inicio,fin,"60",source1)
		DS2 = conexion.GetByFont(poly,inicio,fin,"60",source2)
		stations = Transversal(DS2,DS1,[[1,1],[0,4]],[[4,5],[5,6]],option=fill)
		extraData = GetEmasByDate(puntos,inicio,fin,'24')
		stations = joindata(stations,extraData,[[1,1],[4,4]],[5,6,7,8,9])
	else:
		stations= GetSource(puntos,inicio,fin,source1)
		if(source1=="EMASMAX"):
			extraData = GetEmasByDate(puntos,inicio,fin,'24')
			stations = joindata(stations,extraData,[[1,1],[4,4]],[5,6,7,8,9])

	conexion.CerrarConexion()
	if len(stations) <1:
		return stations
	result,images = Clustering(stations,k,True,0,variables=vari) 
	return result

def GetGraphDates(puntos,inicio,fin):
	conexion = HandlerDB()
	poly =format_polygon(puntos)
	res_emas = conexion.GetByFont(poly,inicio,fin,"60","EMAS")
	res_merra = conexion.GetByFont(poly,inicio,fin,"60","MERRA")
	imagenes = Graphics(res_merra,res_emas) 
	conexion.CerrarConexion()
	return imagenes

def GetGraphStations(puntos,inicio,fin):
	conexion = HandlerDB()
	poly =format_polygon(puntos)
	res_emas = conexion.GetByFont(poly,inicio,fin,"60","EMAS")
	stat = GraphicsEMAS(res_emas) 
	conexion.CerrarConexion()
	return stat

def GraphicsEMAS(data_emas):
	directory=str(random.randint(0,MAX_DIR))
	if not path.exists(base+fout):
		mkdir(base+fout)
	if not path.exists(base+fout+"plots"):
		mkdir(base+fout+"plots")
	if not path.exists(base+fout+"plots/"+directory):
		mkdir(base+fout+"plots/"+directory)

	with open(join(base+fout+"plots/"+directory,"emas.csv"), "w") as file:
		writer = csv.writer(file)
		for e in data_emas:
			writer.writerow(e)  #escribir linea

	#Ejecutar programa en R
	r = requests.get('http://'+IPHost+':'+str(GS_port)+'/stations?folder='+str(directory),verify=False)

	p = base+fout+"plots/"+directory	
	lstDir = walk(p)
	#listar imagenes
	lstStation = []
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = path.splitext(fichero)
			if(extension==".jpeg"):
				lst = []
				lst.append(nombreFichero)
				lst.append(fout+"plots/"+directory+"/"+nombreFichero+extension)
				lstStation.append(lst)
	return lstStation

def Graphics(data_merra,data_emas):
	directory=str(random.randint(0,MAX_DIR))
	if not path.exists(base+fout):
		mkdir(base+fout)
	if not path.exists(base+fout+"plots"):
		mkdir(base+fout+"plots")
	if not path.exists(base+fout+"plots/"+directory):
		mkdir(base+fout+"plots/"+directory)


	with open(join(base+fout+"plots/"+directory,"emas.csv"), "w") as file:
		writer = csv.writer(file)
		for e in data_emas:
			writer.writerow(e)  #escribir linea

	with open(join(base+fout+"plots/"+directory,"merra.csv"), "w") as file:
		writer = csv.writer(file)
		for m in data_merra:
			writer.writerow(m)	#escribir linea

	#Ejecutar programa en R
	r = requests.get('http://'+IPHost+':'+str(GD_port)+'/dates?folder='+str(directory),verify=False)
	#commands.getoutput("Rscript Graphs.R "+directory)

	p = base+fout+"plots/"+directory	
	lstDir = walk(p)
	#listar imagenes

	lstFiles = []
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = path.splitext(fichero)
			print(nombreFichero)
			if(extension == ".png"):
				lstFiles.append(fout+"plots/"+directory	+"/"+nombreFichero+extension)
	return lstFiles

def Summary(polygon, inicio, fin):
	"""
	Obtiene el coeficiente de correlación Pearson, covarianza y varianza
	de la variable temperatura extraida de las fuentes EMAS y MERRA
	"""

	conexion = HandlerDB()
	poly =format_polygon(polygon)

	emast = conexion.GetByFont(poly, inicio, fin, '60', 'EMAS') # al ser de 60 min, los valores de prec, rad o hum, NO SON MEDIAS
	merra = conexion.GetByFont(poly, inicio, fin, '24', 'MERRA')
	conexion.CerrarConexion()
	emas=[]

	temp = 0; id = "0"; MAX=0; MIN=0; MEAN=0; date="0";
	arr=[]
	for e in emast:
		if (temp==0):
			id = e[4] #e[4] es el codigo de la estacion
			date = e[1]
			temp_e = list(e) #se guarda temporalmente el registro
			temp = 1
		if(id==e[4] and date == e[1]):
			if e[5] is not None:
				arr.append(float(e[5]))
		else:
			if len(arr) > 2:
				MAX = np.amax(arr) #los registros de 60 min se concentran en medias, max y min. por estacion
				MIN = np.amin(arr)
				MEAN =np.mean(arr)
				temp_e[5] = MEAN
				temp_e = temp_e + [MAX,MIN]
				emas.append(temp_e)
			arr=[]; 
			if e[5] is not None:
				arr.append(float(e[5]))
			temp_e = list(e); id= e[4]; date = e[1]


	stations = []

	for rowEmas in emas:
		for rowMerra in merra:
			if(rowEmas[4] == rowMerra[0] and rowEmas[1] == rowMerra[1] ):
				station = {
					"codigo": rowMerra[0],
					"fecha": rowEmas[1],
					"latitud": rowEmas[2],
					"longitud": rowEmas[3],
					"temperaturaEmas": rowEmas[5],
					"temp_meanMerra": rowMerra[4],
					"temp_maxMerra": rowMerra[5],
					"temp_minMerra": rowMerra[6],
					"humedadEmas": rowEmas[6],
					"presion_barometricaEmas": rowEmas[7],
					"precipitacionEmas": rowEmas[8],
					"radiacion_solarEmas": rowEmas[9],
					"maximaEmas": rowEmas[11],
					"minimaEmas": rowEmas[12],
				}
				stations.append(station)

	url = 'http://'+S_port+'/api/v1/correlation'
	body = { 'data': stations }
	#params = {'columns': 'temperaturaEmas,temp_meanMerra'}
	params = {'columns': 'maximaEmas,temp_maxMerra'}
	params2 = {'columns': 'minimaEmas,temp_minMerra'}
	result = requests.post(url, data=json.dumps(body), params=params)
	result2 = requests.post(url, data=json.dumps(body), params=params2)
	c = {'MAX':result.json(), 'MIN':result2.json()}

	return c

# --------------- UTILS (FUNCIONES DE UTILERIA) ---------------------

#Transversal function
def Transversal(S1,S2,groupers,variables,option=False):
	TransversalData = []
	T = [None] * len(variables)
	temp = [None] * len(variables)
	for Reg_S1 in S1: # se recorren ambos sources
		trv = False
		for Reg_S2 in S2:
			flag = True
			for g in groupers: ## verificar que un registro cumpla con los agrupamientos
				if(Reg_S1[g[0]]!=Reg_S2[g[1]]):
					flag = False

			if flag==True: # si se cumple con los agrupamientos se realiza la transversalidad
				trv = True
				for index,item in enumerate(variables):
					T[index] = Diferential(Reg_S1[item[0]],Reg_S2[item[1]]) #funcion transversal "KERNEL"
					temp[index] = Reg_S1[item[0]]
				#una vez aplicado, los resultados se agregan
				TransversalData.append(tuple(list(Reg_S2) + temp + T + [Reg_S1[6]])) # AQUI HAY COSAS HARDCOVARIABLES REG1)
				break
		if trv==False and option==True: #en caso de no encontrar valores en el otro conjunto, esto es una condicion aparte
			# se puede omitir o cambiar
			TransversalData.append(tuple([Reg_S1[0],Reg_S1[1],Reg_S1[2],Reg_S1[3],Reg_S1[0],99999,99999,Reg_S1[4],Reg_S1[5],99999,99999,Reg_S1[6]]))

	return TransversalData


def joindata(S1,S2,groupers,variables):
	data = []
	for Reg_S1 in S1:
		items = []
		for Reg_S2 in S2:
			flag=True
			for g in groupers: ## verificar que un registro cumpla con los agrupamientos
				if(Reg_S1[g[0]]!=Reg_S2[g[1]]):
					flag = False
			if flag == True:
				for v in variables:
					items = items+ [Reg_S2[v]]
				data.append(list(Reg_S1)+items)
				break
		if flag==False:
			data.append(list(Reg_S1)+["NA","NA","NA","NA","NA"]) #esto esta harcodeado
	return data


def Diferential(a,b):
	try:
		if (a=="Null" or b=="Null"):
			return None
		else:
			return float(a)-float(b)
	except Exception as e:
		return None

def format_polygon(poligono):
	poly ="("
	for i in range(1,len(poligono)+1):
		poly = poly+"("+str(poligono[str(i)]['lon'])+","+str(poligono[str(i)]['lat'])+"),"
	poly = poly[:-1] +")" 
	return poly

def format_variables(variables,status):
	lista = ""
	if len(variables)<0: lista= "10,"
	for v in variables:
		if status == "EMASMAX":
			if v == "Temp_max_emas": lista=lista+"5,"
			if v == "Temp_min_emas": lista=lista+"6,"
			if v == "Humedad": lista=lista+"8,"
			if v == "Precipitacion": lista=lista+"10',"
			if v == "Presion_barometrica": lista=lista+"9,"
			if v == "Radiacion_solar": lista=lista+"11,"
		elif status == "MERRA":
			if v == "Temp_max_merra": lista=lista+"4,"
			if v == "Temp_min_merra": lista=lista+"5,"
		elif status == "DIFERENCIAL":
			if v == "Temp_max_emas": lista=lista+"5,"
			if v == "Temp_min_emas": lista=lista+"6,"
			if v == "Temp_max_merra": lista=lista+"7,"
			if v == "Temp_min_merra": lista=lista+"8,"
			if v == "Differential_max": lista=lista+"9,"
			if v == "Differential_min": lista=lista+"10,"
			if v == "Humedad": lista=lista+"13,"
			if v == "Precipitacion": lista=lista+"15,"
			if v == "Presion_barometrica": lista=lista+"14,"
			if v == "Radiacion_solar": lista=lista+"16,"
	return lista[:-1]

def arr2json(arr):
	jsontable=dict(); j=0
	for x in arr:
		registro=dict(); i = 1
		for col in x:
			registro[i]=col
			i+=1
		jsontable[j]=registro
		j+=1
	return jsontable
		


# --------------- 		AaS (As a Service) ---------------------

def Summary_service(stations,params):
	body = { 'data': stations }

	url = 'http://'+IPHost+':'+S_port+'/api/v1/correlation'
	result = requests.post(url, data=json.dumps(body), params=params)
	return result.json()

# --------------- 		AaS (As a Service) ---------------------

def TwoChoises(choices_list):
	#actually
	workers_list = list(choices_list)
	fc = random.choice(workers_list)
	sc = random.choice(workers_list)
	wlfc = len(choices_list[fc])
	wlsc = len (choices_list[sc])
	if wlfc >wlsc:
		return fc
	else:
		return sc

def RandomChoice(choices_list):
	#actually
	fc = random.choice(choices_list)
	return fc