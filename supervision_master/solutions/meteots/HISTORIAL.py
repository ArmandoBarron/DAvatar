from HandlerDB import *

 
def GetMerraByDate(puntos,inicio,fin,hora = ""):
    conexion = HandlerDB()
    poly = ""
    result = conexion.GetByFont(poly,inicio,fin,hora,"MERRA")
    conexion.CerrarConexion()
    return result



#anios = [1982,1983,1984,1985,1986,1987,1988,1989,1990]
#anios = [1980,1981]
anios = [1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011]

for a in anios:
    inicio = "01/01/"+str(a)
    fin = "31/12/"+str(a)
    result = GetMerraByDate("",inicio,fin,hora="all")
    stations =[]
    ids=result[0][0];counter=0;cMAX=0;cMIN=0;cMEAN=0;
    conexion = HandlerDB()
    print(len(result))
    e=0
    for estacion in result:  
        if(ids==estacion[0]):
            cMAX+=estacion[4]
            cMIN+=estacion[5]
            cMEAN+=estacion[6]
            t_lat=estacion[2]
            t_lon=estacion[3]
            counter+=1
        else:
            data= [ a,ids,t_lat,t_lon,cMAX/counter,cMIN/counter,cMEAN/counter]
            stations.append(data)
            ids=estacion[0]
            cMAX=estacion[4]
            cMIN=estacion[5]
            cMEAN=estacion[6]
            t_lat=estacion[2]
            t_lon=estacion[3]
            counter=1
            conexion.InsertarFilas(data)
            e+=1
            print(e)
    conexion.commit()
    conexion.CerrarConexion()


