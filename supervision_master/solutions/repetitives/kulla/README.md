# demo-kulla-master-slave

Contiene la implementación del patrón Master/Slave utilizando el modelo de Kulla.

## Acerca de este repositorio

Listado de archivos:

* **MasterSlave/** Carpeta que contiene el código del Master y el Slave implementados utilizando el modelo de Kulla.
  * *AES-Libraries/* Contiene las bibliotecas necesarias para que la aplicación *AESCode* funcione correctamente.
  * *LZ4-Libraries/* Contiene las bibliotecas necesarias para que la aplicación *LZ4Compressor* funcione correctamente.
  * *Kulla-Libraries/* Contiene las aplicaciones *Master* y *Slave* funcionen correctamente.
  * *Logs/* Contendrá los Logs producidos por las aplicaciones
  * *AESCode.c* Permite realizar el cifrado de datos almacenados en memoria compartida utilizando AES
  * *GenerateSHA256.c* Permite generar el hash de datos almacenados en memoria compartida utilizando SHA-256 y lo concatena al inicio del mismo
  * *LZ4Compressor.c* Comprime datos almacenados en memoria compartida utilizando el algoritmo de compresión sin perdidas LZ4
  * *Makefile* Contiene los comandos requeridos para compilar las aplicaciones
  * *Master.c* Contiene el código que realiza las funciones de Master, crea w hilos, a cada hilo le asigna una lista de archivos que debe procesar. El hilo incia el procesamiento de los datos invocando a la aplicación Slave, la cual es responsable de aplicar los mismos procesos a cada contenido. 
  * *Slave.c* Recibe una ruta de entrada y una ruta de salida. Realiza la lectura de los datos de entrada y ejecuta la tubería compuesta por los filtros: SHA-256, LZ4, AES. Al finalizar realiza la escritura del resyltado en la ruta de salida
* **Dockerfile** Archivo con los comandos requeridos para construir la imagen de contenedor con las dependencias del patrón
* **Readme.md** Este archivo

## Realizar una prueba rápida

### Crear imagen de contenedor

```bash
docker build -f Dockerfile -t hgreyesa/masterslave .
```

En dónde:

* *docker build*: indica que se realizará una construcción de imagen de contenedor

* *-f*: indica el nombre del archivo Dockerfile que será usado para contruir la imagen de contenedor. Si esta bandera se omite, la plataforma busca el archivo con el nombre "Dockerfile". 

* *Dockerfile*: es el nombre del archivo Dockerfile que será usado para crear la imagen de contenedor, puede ser otro nombre distinto al por defecto

* *-t*: indica que se le asignará un nombre a la imagen de contenedor

* *hgreyesa/masterslave*: Es el nombre que se le asignará a la imagen de contenedor

* *.* : Indica el directorio que se usará como contexto (el directorio que contiene el dockerfile)

### Lanzar un contenedor

A continuación se muestra un ejemplo del comando requerido para crear un contenedor virtual que contenga el patrón master/slave.

```
docker run -dti --name masterSlave \
-v /media/hreyes/Data/Volumenes/img/:/home/Volumen/Source/ \
-v /media/hreyes/Data/Volumenes/sink/:/home/Volumen/Sink/ \
hgreyesa/masterslave
```

**Notas**

* Cambiar la ruta */media/hreyes/Data/Volumenes/img/* por la ruta que contenga los datos que desees procesar.
* Cambiar la ruta */media/hreyes/Data/Volumenes/sink/* por la ruta en la que desee almacenar los resultados.

### Ejecutar el manager

1. Con 1 trabajador

   ```bash
   docker exec -ti masterSlave ./Master /home/Volumen/Source/ /home/Volumen/Sink/ 1
   ```

2. Con 4 trabajadores

   ```bash
   docker exec -ti masterSlave ./Master /home/Volumen/Source/ /home/Volumen/Sink/ 4
   ```

### Mostrar las bitácoras

```bash
docker exec -ti masterSlave bash
cat Logs/Worker_*
```

