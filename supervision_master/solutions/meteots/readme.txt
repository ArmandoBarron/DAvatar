
ANTES DE EJECUTAR:
	modificar config ini por la ip local en el apartado de servicios
	algunos servicios ocupan de la ip local para accederse.

PARA EJECUTAR LOS MICROSERVICIOS:
docker-compose up -d

PARA RECONSTRUIR IMAGENES:
docker-compose up -d --build


LOS MICROSERVICIOS SE ENCUENTAN EN LA CARPETA RSERVICES
IMAGENES O RESULTADOS GENERADOS POR LOS SERVICIOS VAN A LA CARPETA static



ejemplo de json a enviar:

{"polygon":{"1":{"lat":"26.29824","lon":"-105.14286"},
 "2":{"lat":"25.5473","lon":"-98.68289"},
 "3":{"lat":"21.64201","lon":"-97.97977"}
 },
"inicio":"20/05/2019",
"fin":"25/05/2019",
"K":0,
"type":1,
 "fuentes":"EMASMAX,MERRA",
 "variables":"Temp_max_emas,Temp_min_emas",
 
}


\getEmas
ejemplo de json a enviar:
{"polygon":{"1":{"lat":"26.29824","lon":"-105.14286"},
 "2":{"lat":"25.5473","lon":"-98.68289"},
 "3":{"lat":"21.64201","lon":"-97.97977"}
 },
"inicio":"01/02/2019",
"fin":"4/02/2019",
"hora":"10:10"
}





