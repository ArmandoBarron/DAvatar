import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

#now.time().strftime('%H:%M:%S')
data = []

data.append((dt.datetime(2021, 6, 29, 0, 0, 0, 0), dt.datetime(2021, 6, 29, 0, 0, 1, 220000), 'tarea1'))

cont1 = 1
minn = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 1, 220000), dt.datetime(2021, 6, 29, 0, 0, 1, 500000), 'tarea2'))
for i in range(0,589):
    cont1 = cont1 + 1
    data.append((dt.datetime(2021, 6, 29, 0, minn, cont1, 220000), dt.datetime(2021, 6, 29, 0, minn, cont1, 500000), 'tarea2'))
    if(cont1 == 59):
        cont1 = 0
        minn = minn + 1

cont1 = 1
minn = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 1, 220000), dt.datetime(2021, 6, 29, 0, 0, 1, 900000), 'tarea3'))
for i in range(0,119):
    cont1 = cont1 + 5
    if(cont1 == 61):
        cont1 = 0
        minn = minn + 1
    if(cont1 == 60):
        cont1 = 0
        minn = minn + 1
    data.append((dt.datetime(2021, 6, 29, 0, minn, cont1, 220000), dt.datetime(2021, 6, 29, 0, minn, cont1, 900000), 'tarea3'))

cont1 = 1
minn = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 1, 220000), dt.datetime(2021, 6, 29, 0, 0, 1, 900000), 'tarea4'))
for i in range(0,59):
    cont1 = cont1 + 10
    if(cont1 == 61):
        cont1 = 0
        minn = minn + 1
    if(cont1 == 60):
        cont1 = 0
        minn = minn + 1
    data.append((dt.datetime(2021, 6, 29, 0, minn, cont1, 220000), dt.datetime(2021, 6, 29, 0, minn, cont1, 900000), 'tarea4'))

cont1 = 3
cont2 = 0
cont3 = 0
cont4 = 0
minn1 = 0
minn2 = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 1, 220000), dt.datetime(2021, 6, 29, 0, 0, 3, 0), 'tarea5'))
for i in range(0,45):
    cont1 = cont1 + 11
    cont2 = cont2 + 200000
    #minn1 = minn1 + 1
    if(cont2 >= 1000000):
        restt = cont2 - 1000000
        cont2 = restt
        cont1 = cont1 + 1
    if(cont1 >= 60): 
        print("hola")
        print(cont1)
        restt = cont1 - 60
        cont1 = restt
        minn1 = minn1 + 1
        if(cont1 >= 60):
            restt = cont1 - 60
            cont1 = restt
            minn1 = minn1 + 1

    cont3 = cont1
    cont3 = cont3 + 1
    cont4 = cont2 
    cont4 = cont4 + 800000
    minn2 = minn1

    if(cont4 >= 1000000):
        restt = cont4 - 1000000
        cont4 = restt
        cont3 = cont3 + 1
    if(cont3 >= 60):
        restt = cont3 - 60
        cont3 = restt
        minn2 = minn2 + 1
    print(cont1)
    print(str(minn1) + "-" + str(cont1) + "-" + str(cont2) + "************" + str(minn2) + "-" + str(cont3) + "-" + str(cont4))
    data.append((dt.datetime(2021, 6, 29, 0, minn1, cont1, cont2), dt.datetime(2021, 6, 29, 0, minn2, cont3, cont4), 'tarea5'))   
    cont1 = cont3
    cont2 = cont4
    minn1 = minn2

cont1 = 13
cont2 = 0
cont3 = 0
cont4 = 0
minn1 = 0
minn2 = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 3, 0), dt.datetime(2021, 6, 29, 0, 0, 13, 0), 'tarea6'))
for i in range(0,45):
    cont1 = cont1 + 3
    cont2 = cont2 + 0
    if(cont2 >= 1000000):
        restt = cont2 - 1000000
        cont2 = restt
        cont1 = cont1 + 1
    if(cont1 >= 60):
        restt = cont1 - 60
        cont1 = restt
        minn1 = minn1 + 1

    cont3 = cont1
    cont3 = cont3 + 10
    cont4 = cont2 
    cont4 = cont4 + 0
    minn2 = minn1

    if(cont4 >= 1000000):
        restt = cont4 - 1000000
        cont4 = restt
        cont3 = cont3 + 1
    if(cont3 >= 60):
        restt = cont3 - 60
        cont3 = restt
        minn2 = minn2 + 1
    #print(str(minn1) + "-" + str(cont1) + "-" + str(cont2) + "************" + str(minn2) + "-" + str(cont3) + "-" + str(cont4))
    data.append((dt.datetime(2021, 6, 29, 0, minn1, cont1, cont2), dt.datetime(2021, 6, 29, 0, minn2, cont3, cont4), 'tarea6'))   
    cont1 = cont3
    cont2 = cont4
    minn1 = minn2

cont1 = 14
cont2 = 200000
cont3 = 0
cont4 = 0
minn1 = 0
minn2 = 0
data.append((dt.datetime(2021, 6, 29, 0, 0, 13, 0), dt.datetime(2021, 6, 29, 0, 0, 14, 200000), 'tarea7'))
for i in range(0,45):
    cont1 = cont1 + 11
    cont2 = cont2 + 800000
    if(cont2 >= 1000000):
        restt = cont2 - 1000000
        cont2 = restt
        cont1 = cont1 + 1
    if(cont1 >= 60):
        restt = cont1 - 60
        cont1 = restt
        minn1 = minn1 + 1

    cont3 = cont1
    cont3 = cont3 + 1
    cont4 = cont2 
    cont4 = cont4 + 200000
    minn2 = minn1

    if(cont4 >= 1000000):
        restt = cont4 - 1000000
        cont4 = restt
        cont3 = cont3 + 1
    if(cont3 >= 60):
        restt = cont3 - 60
        cont3 = restt
        minn2 = minn2 + 1
    #print(str(minn1) + "-" + str(cont1) + "-" + str(cont2) + "************" + str(minn2) + "-" + str(cont3) + "-" + str(cont4))
    data.append((dt.datetime(2021, 6, 29, 0, minn1, cont1, cont2), dt.datetime(2021, 6, 29, 0, minn2, cont3, cont4), 'tarea7'))   
    cont1 = cont3
    cont2 = cont4
    minn1 = minn2

"""data = [    (dt.datetime(2021, 6, 29, 0, 0, 0, 0), dt.datetime(2021, 6, 29, 0, 0, 1, 22), 'tarea1'),
            (dt.datetime(2021, 6, 29, 0, 2, 5, 34), dt.datetime(2021, 6, 29, 0, 4, 6, 0), 'tarea2'),
            (dt.datetime(2021, 6, 29, 0, 5, 0, 0), dt.datetime(2021, 6, 29, 0, 6, 2, 0), 'Almacenar Datos'),
            (dt.datetime(2021, 6, 29, 0, 2, 5, 34), dt.datetime(2021, 6, 29, 0, 4, 6, 0), 'tarea6'),
            (dt.datetime(2021, 6, 29, 0, 5, 0, 0), dt.datetime(2021, 6, 29, 0, 6, 2, 0), 'tarea7'),
            (dt.datetime(2021, 6, 29, 0, 6, 3, 0), dt.datetime(2021, 6, 29, 0, 8, 4, 0), 'tarea2'),
            (dt.datetime(2021, 6, 29, 0, 8, 6, 0), dt.datetime(2021, 6, 29, 0, 9, 6, 0), 'Almacenar Datos'), 
            (dt.datetime(2021, 6, 29, 0, 8, 6, 0), dt.datetime(2021, 6, 29, 0, 9, 6, 0), 'tarea6')
        ]"""


cats = {"tarea1" : 1, "tarea2" : 2, "tarea3" : 3, "tarea4": 4, "tarea5" : 5, "tarea6": 6, "tarea7":7}
colormapping = {"tarea1" : "C5", "tarea2" : "C1", "tarea3" : "C2", "tarea4": "C3", "tarea5" : "C4", "tarea6": "C9", "tarea7": "C6"}

verts = []
colors = []



for d in data:
    v =  [(mdates.date2num(d[0]), cats[d[2]]-.4),
          (mdates.date2num(d[0]), cats[d[2]]+.4),
          (mdates.date2num(d[1]), cats[d[2]]+.4),
          (mdates.date2num(d[1]), cats[d[2]]-.4),
          (mdates.date2num(d[0]), cats[d[2]]-.4)]
    verts.append(v)
    colors.append(colormapping[d[2]])

#print(colors)

bars = PolyCollection(verts, facecolors=colors)


#fig= plt.figure(figsize=(9,3))
fig, ax = plt.subplots(figsize=(13,5))
ax.add_collection(bars)
ax.autoscale()
#loc = mdates.MicrosecondLocator(interval=1, tz=None)
loc = mdates.SecondLocator(bysecond=[0])
#loc = mdates.MinuteLocator(byminute=[0])
ax.xaxis.set_major_locator(loc)
#ax.xaxis.set_major_formatter(mdates.AutoTimeFormatter(loc))
#ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))
formatter = mdates.AutoDateFormatter(loc)
#formatter.scaled[1/(24.*60.)] = '%H:%S'
ax.xaxis.set_major_formatter(formatter)
ax.set_yticks([1,2,3,4,5,6,7])
ax.set_yticklabels(["tarea1", "tarea2", "tarea3", "tarea4", "tarea5", "tarea6", "tarea7"],fontsize=13) 
ax.set_xlabel("Línea de tiempo en minutos", fontsize=13)
plt.savefig('plot.pdf',bbox_inches='tight')
#plt.show()