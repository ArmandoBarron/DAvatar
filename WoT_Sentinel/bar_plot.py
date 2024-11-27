from os import error
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

#pinkBars = getData
#orangeBars = representation
#blueBars = store 



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

plotdata = pd.DataFrame({
    'ServiceTime-Representation': [0.000463247,0.001055956,0.00113225,0.002645969,0.005290985,0.006728378,0.015782739,0.021732901,0.057381936]
    }, 
    index=["vc1-dst1","vc5-dst1","vc1-dst5","vc10-dst1","vc5-dst5","vc1-dst10","vc10-dst5","vc5-dst10","vc10-dst10"]
)

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



"""plotdata.plot(kind="bar")
plt.xlabel("Número de contenedores virtuales por sistema")
plt.ylabel("Tiempo en segundos")"""

plotdata.plot(kind="bar")
plt.xlabel("Number of virtual containers per DST")
plt.ylabel("Time in seconds")

# Show graphic
plt.savefig('plot.pdf',bbox_inches='tight')
#fig = plt.subplots(figsize=(13,5))

#plt.subplots(figsize=(13,5))
#plt.show()
#plt.show()