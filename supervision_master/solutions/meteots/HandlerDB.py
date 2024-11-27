import psycopg2
import psycopg2.extras
from datetime import datetime
from datetime import timedelta
import configparser

class HandlerDB:

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		host=config['Database']['host']
		user= config['Database']['user']
		pw=config['Database']['pass']
		DB= config['Database']['DB']
		puerto= config['Database']['port']

		self.state= config['Database']['state']

		self.mydb = psycopg2.connect(
		host=host,
		user=user,
		password=pw,
		database=DB,
		port = int(puerto)
		)
		self.mycursor = self.mydb.cursor()

	def GetByFont(self,poligono,inicio,fin,hora,font):
		if font == "EMASMAX":
			query = "select data_60m.estacion,data_60m.fecha, data_60m.latitud,data_60m.longitud,data_60m.codigo,\
					max(CAST(data_60m.temperatura as FLOAT)) as max_emas,\
					min(CAST(data_60m.temperatura as FLOAT)) as min_emas\
					from data_60m where \
					polygon(%s) @> point(''||data_60m.longitud||','||data_60m.latitud||'') and \
					to_date(data_60m.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(data_60m.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY') \
					group by data_60m.fecha,data_60m.estacion,data_60m.codigo,data_60m.latitud,data_60m.longitud \
					order by fecha"			 	
			self.mycursor.execute(query, (poligono,inicio,fin,))
			result = self.mycursor.fetchall()
			return result

		if font == "EMAS":
			if hora =="60":
				query = "select data_60m.estacion,data_60m.fecha, data_60m.latitud,data_60m.longitud,data_60m.codigo,data_60m.temperatura,\
					data_60m.humedad,data_60m.presion_barometrica,data_60m.precipitacion,data_60m.radiacion_solar,data_60m.hora\
					from data_60m where \
					polygon(%s) @> point(''||data_60m.longitud||','||data_60m.latitud||'') and \
					to_date(data_60m.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(data_60m.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY')\
					order by data_60m.codigo,data_60m.fecha"			 	
				self.mycursor.execute(query, (poligono,inicio,fin,))
				result = self.mycursor.fetchall()
				return result
			elif hora =="10":
				query = "select data_10m.estacion,data_10m.fecha, data_10m.latitud,data_10m.longitud,data_10m.codigo,data_10m.temperatura,\
					data_10m.humedad,data_10m.presion_barometrica,data_10m.precipitacion,data_10m.radiacion_solar\
					from data_10m where \
					polygon(%s) @> point(''||data_10m.longitud||','||data_10m.latitud||'') and \
					to_date(data_10m.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(data_10m.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY')\
					order by data_10m.codigo"	
				self.mycursor.execute(query, (poligono,inicio,fin,))
				result = self.mycursor.fetchall()
				return result
			elif hora =="24":
				query = "select data_24h.estacion,data_24h.fecha, data_24h.latitud,data_24h.longitud,data_24h.codigo,data_24h.temperatura,\
					data_24h.humedad,data_24h.presion_barometrica,data_24h.precipitacion,data_24h.radiacion_solar\
					from data_24h where \
					polygon(%s) @> point(''||data_24h.longitud||','||data_24h.latitud||'') and \
					to_date(data_24h.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(data_24h.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY')\
					order by fecha"			 	
				self.mycursor.execute(query, (poligono,inicio,fin,))
				result = self.mycursor.fetchall()
				return result
			else:
				query = "select data_10m.estacion,data_10m.fecha, data_10m.latitud,data_10m.longitud,data_10m.codigo,data_10m.temperatura,\
					data_10m.humedad,data_10m.presion_barometrica,data_10m.precipitacion,data_10m.radiacion_solar\
					from data_10m where \
					polygon(%s) @> point(''||data_10m.longitud||','||data_10m.latitud||'') and \
					to_date(data_10m.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(data_10m.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY')\
					and data_10m.hora::time(0) = %s::time(0) \
					order by fecha"			 	
				self.mycursor.execute(query, (poligono,inicio,fin,hora,))
				result = self.mycursor.fetchall()
				return result

		elif font == "MERRA":
			if hora == "all":
				query = "select station_code, fecha,latitud,longitud, temp_max as max,temp_min as min ,temp_mean as mean from merra_historico where \
					to_date(fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
					to_date(fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY') \
					Group by station_code,fecha,latitud,longitud,max,min,mean\
					order by station_code"
				self.mycursor.execute(query, (inicio,fin,))
				result = self.mycursor.fetchall()
				return result
			elif hora =="year":
				query = "select station_code, año,latitud,longitud, temp_max as max,temp_min as min ,temp_mean as mean from merra_year where \
						polygon(%s) @> point(''||longitud||','||latitud||'') and\
						año > %s and año< %s order by station_code"
				self.mycursor.execute(query, (poligono, inicio,fin,))
				result = self.mycursor.fetchall()
				return result			
			else:
				query = "select merra.station_code,merra.fecha, merra.latitud,merra.longitud,merra.temp_max,\
				merra.temp_min,merra.temp_mean \
				from merra where \
				polygon(%s) @> point(''||merra.longitud||','||merra.latitud||'') and\
				to_date(merra.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
				to_date(merra.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY') \
				order by fecha"
				self.mycursor.execute(query, (poligono,inicio,fin,))
				result = self.mycursor.fetchall()
				return result
		else:
			return False


	def GetInsidePolygon(self,poligon,date):
		query = "select antenas.antena,antenas.latitud,antenas.longitud,antenas.codigo,data_24h.temperatura,merra.temp_mean,data_24h.humedad from antenas,data_24h,merra where \
			polygon(%s) @> point(''||antenas.longitud||','||antenas.latitud||'')  \
			and data_24h.fecha=%s and merra.fecha=%s \
			and antenas.codigo = data_24h.codigo \
			and merra.station_code = data_24h.codigo order by codigo"
		self.mycursor.execute(query, (poligon,date,date,))
		result = self.mycursor.fetchall()
		return result


	def GetInsidePolygonDict(self,poligon,date):
		query = "select antenas.antena,antenas.latitud,antenas.longitud,antenas.codigo,data_24h.temperatura,merra.temp_mean,data_24h.humedad from antenas,data_24h,merra where \
			polygon(%s) @> point(''||antenas.longitud||','||antenas.latitud||'')  \
			and data_24h.fecha=%s and merra.fecha=%s \
			and antenas.codigo = data_24h.codigo \
			and merra.station_code = data_24h.codigo order by codigo"
		cursor = self.mydb.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(query, (poligon,date,date,))
		colnames = [desc[0] for desc in cursor.description]
		result = cursor.fetchall()
		puntos = []
		for row in result:
			punto = {}
			for col in colnames:
				punto[col] = row[col]
			puntos.append(punto)
		return puntos


	def GetInsidePolygonMonth(self,poligon,date,month):
		query = "select antenas.antena,antenas.latitud,antenas.longitud,antenas.codigo,data_24h.temperatura,merra.temp_mean,data_24h.humedad from antenas,data_24h,merra where \
			polygon(%s) @> point(''||antenas.longitud||','||antenas.latitud||'')  \
			and data_24h.fecha like '%/%s/%' and merra.fecha='%/%s/% \
			and antenas.codigo = data_24h.codigo \
			and merra.station_code = data_24h.codigo order by codigo"
		self.mycursor.execute(query, (poligon,date,date,))
		result = self.mycursor.fetchall()
		return result

	def GetInsideDateRange(self,poligon,inicio,fin):
		query = "Select antenas.antena,data_60m.fecha,antenas.latitud,antenas.longitud,antenas.codigo,max(CAST(data_60m.temperatura as FLOAT)) \
			as max_emas,min(CAST(data_60m.temperatura as FLOAT)) as min_emas, \
			merra.temp_max as max_merra, merra.temp_min as min_merra, \
			(merra.temp_max- max(CAST(data_60m.temperatura as FLOAT))) as max_diferencial, \
			(merra.temp_min- min(CAST(data_60m.temperatura as FLOAT))) as min_diferencial\
			from merra,data_60m,antenas\
			where \
			polygon(%s) @> point(''||antenas.longitud||','||antenas.latitud||'') and \
			data_60m.fecha=merra.fecha and \
			merra.station_code=data_60m.codigo and \
			antenas.codigo = data_60m.codigo and \
			to_date(data_60m.fecha,'DD-MM-YYYY') >= to_date(%s,'DD-MM-YYYY') and \
			to_date(data_60m.fecha,'DD-MM-YYYY') <= to_date(%s,'DD-MM-YYYY')\
			group by \
			data_60m.fecha,antenas.antena,antenas.latitud,antenas.longitud,merra.temp_max, merra.temp_min,antenas.codigo"
		self.mycursor.execute(query, (poligon,inicio,fin,))
		result = self.mycursor.fetchall()
		return result

	def commit(self):
		self.mydb.commit()

	def CerrarConexion(self):
		self.mycursor.close()
		self.mydb.close()

	def InsertarFilas(self,row):
		self.mycursor.execute('INSERT INTO merra_year(año,station_code,latitud, \
					longitud, temp_max,temp_min, temp_mean) \
					VALUES(%s, %s, %s, %s, %s, %s, %s)', 
					row)