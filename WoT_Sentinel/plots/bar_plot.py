from os import error
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

#pinkBars = getData
#orangeBars = representation
#blueBars = store 



#vc1-dst1 . vc5-dst1 . vc1-dst5 . vc10-dst1 . vc1-dst10 . vc5-dst5 . vc5-dst10 . vc10-dst10

##################################
#MemApp
"""plotdata = pd.DataFrame({
    'ST - Obtener datos': [0.139677008,1.115425539,1.208801985,2.630154848,2.873927332,6.246092782,12.27381982,26.19203892],
    'ST - Almacenar': [0.066992683,0.532629013,0.484360218,1.278212078,1.3016387242,3.089240109,5.018638227,9.973927461],
    'RT': [0.207736929,1.650381517,1.695852041,3.911986828,4.179668904,9.348770444,17.33143288,36.22780551]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""

"""plotdata = pd.DataFrame({
    'ST - Representación': [0.000483274,0.002326965,0.002293109,0.003123999,0.004102848,0.013437553,0.038974829,0.061839132]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""
###################################

##################################
#FsApp
"""plotdata = pd.DataFrame({
    'ST - Obtener datos': [0.133762836,0.724690199,0.694983006,1.523810239,1.643810287,3.574916508,7.347380925,14.88786628],
    'ST - Almacenar': [0.084852934,0.158522129,0.229831696,0.357281726,0.387452982,1.219157423,2.768481934,4.898342653],
    'RT': [0.21942091,0.885175705,0.926190853,1.883674697,2.034446006,4.799695275,10.13778829,20.21234183]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""

plotdata = pd.DataFrame({
    'ST - Representación': [0.000439882,0.001382828,0.001105547,0.002582732,0.003182737,0.005621344,0.021925428,0.0426132899]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)
###################################

##################################
#NetApp
"""plotdata = pd.DataFrame({
    'ST - Obtener datos': [0.131305933,0.688092947,0.762892008,1.426185733,1.481376329,3.734823012,8.001298745,13.10352887],
    'ST - Almacenar': [0.084852934,0.242475033,0.408089876,0.514939883,0.578739238,2.160479283,4.856827492,8.029382427],
    'RT': [0.199519873,0.931838036,1.172472,1.943574236,2.063264439,5.902005482,12.87310922,21.16954078]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""

plotdata = pd.DataFrame({
    'ST - Representación': [0.000427961,0.00092411,0.001221895,0.00244862,0.003148872,0.006703187,0.014982983,0.036629482]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)
###################################

##################################
#CpuApp
"""plotdata = pd.DataFrame({
    'ST - Obtener datos': [0.135978937,0.793085098,0.737254143,1.729482034,1.982381035,4.001849573,7.017138233,14.17638402],
    'ST - Almacenar': [0.073806763,0.230095148,0.332326174,0.552482103,0.722432384,1.851608475,3.599283829,7.568240385],
    'RT': [0.210601091,1.024637938,1.071233034,2.28452038,2.708266171,5.86084147,10.63277699,21.77491924]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""

"""plotdata = pd.DataFrame({
    'ST - Representación': [0.000521898,0.001028061,0.001396656,0.002556243,0.003452752,0.007383422,0.016354924,0.030294839]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""
###################################

##################################
#ECG Sensors
plotdata = pd.DataFrame({
    'ST - Obtener datos': [0.14144206,0.681561708,0.687786341,1.295197964,1.350820383,3.155329466,6.582739139,13.89273823],
    'ST - Almacenar': [0.067327023,0.212248087,0.301664591,0.463975191,0.501837468,0.863109589,1.858202817,4.052619309],
    'RT': [0.209470987,0.895479918,0.990833044,1.762124062,1.859386229,4.024005175,8.462674857,18.00273948]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)

"""plotdata = pd.DataFrame({
    'ST - Representación': [0.000463247,0.001055956,0.00113225,0.002645969,0.006728378,0.005290985,0.021732901,0.057381936]
    }, 
    index=['vc1-dst1','vc5-dst1','vc1-dst5','vc10-dst1','vc1-dst10','vc5-dst5','vc5-dst10','vc10-dst10']
)"""
###################################

"""plotdata = pd.DataFrame({
    'ServiceTime-GetData': [0.14144206,0.681561708,1.295197964,2.67427516,6.032924929,13.67263891],
    'ServiceTime-StoreData': [0.067327023,0.212248087,0.463975191,0.947584629,1.821738192,3.84729382],
    'ResponseTime': [0.209470987,0.895479918,1.762124062,3.626260042,7.87044586,17.55722663]
    }, 
    index=['1','5','10','20','50','100']
)"""

"""plotdata = pd.DataFrame({
    'TiempoServicio-ObtenerDatos': [0.14144206,0.681561708,1.295197964,2.67427516,6.032924929,13.67263891],
    'TiempoServicio-AlmacenarDatos': [0.067327023,0.212248087,0.463975191,0.947584629,1.821738192,3.84729382],
    'TiempoRespuesta': [0.209470987,0.895479918,1.762124062,3.626260042,7.87044586,17.55722663]
    }, 
    index=['1','5','10','20','50','100']
)"""

"""plotdata = pd.DataFrame({
    'ServiceTime-Representation': [0.000463247,0.001055956,0.00113225,0.002645969,0.005290985,0.006728378,0.015782739,0.021732901,0.057381936]
    }, 
    index=["vc1-dst1","vc5-dst1","vc1-dst5","vc10-dst1","vc5-dst5","vc1-dst10","vc10-dst5","vc5-dst10","vc10-dst10"]
)"""

"""plotdata = pd.DataFrame({
    'TiempoServicio-Representación': [0.000463247,0.001055956,0.00113225,0.002645969,0.005290985,0.006728378,0.015782739,0.021732901,0.057381936]
    }, 
    index=["cv1-scv1","cv5-scv1","cv1-scv5","cv10-scv1","cv5-scv5","cv1-scv10","cv10-scv5","cv5-scv10","cv10-scv10"]
)"""

"""plotdata = pd.DataFrame({
    'ServiceTime-GetData': [0.872714996],
    'ServiceTime-StoreData': [0.334915161],
    'ServiceTime-Representation': [0.002938986],
    'ResponseTime': [1.210872889]
    }, 
    index=["vc3-s2"]
)"""

#data = (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)

"""data = (0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.045,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.176,0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.176,0.176,0.176,0.045,0.045,0.045,0.045,1.119,1.119,1.119,1.119)"""
"""
ind = np.arange(len(data))  # the x locations for the groups
width = 0.20  # the width of the bars
fig, ax = plt.subplots(figsize=(13,5))
rects1 = ax.bar(ind - width/2, data, width)
#plt.yticks((0,1))
ax.set_xlabel("Requests to DST", fontsize=13)
#ax.set_ylabel('Kilobits received', fontsize=13)
ax.set_xticks(ind)
#x.legend()

fig.tight_layout()"""



plotdata.plot(kind="bar")
plt.xlabel("Número de contenedores virtuales por DST")
plt.ylabel("Tiempo en segundos")

"""plotdata.plot(kind="bar")
plt.xlabel("Number of virtual containers per DST")
plt.ylabel("Time in seconds")"""

# Show graphic
plt.savefig('build-ecgapp.pdf',bbox_inches='tight')
#fig = plt.subplots(figsize=(13,5))

#plt.subplots(figsize=(13,5))
#plt.show()
#plt.show()