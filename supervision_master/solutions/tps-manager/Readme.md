# Configuracion para el uso de los TPS y DAGSINK

* Abir archivo Sourcefile.sourceme
* Cambiar las  IP por la adecuada (para prueba en local usar la ip local NO LOCALHOST)
* Cambiar ubicacion de FTP_PUBLUSHED_FOLDER. Esta es la carpeta donde estan los datos producidos por el engine (e.g lo que es lo mismo que el scratch_dir_base de DagOn). Para evitar errores, terminar la ruta siempre con "/".
* Guardar archivo y ejecutar
    > source Sourcefile.sourceme

    > docker-compose up --build

Estos comandos configuraran el entorno de los TPS, los monitores y otros servicios. 

# Usando DagOn* (python3) con transversal
Para usar el transversal es posible a ravez de 2 formas: utilizando la libreria WITE o la version modificada de DagOn.
Para usar DagOn* ir a la carpeta ./WITE/Engines/dagonstar/

* Abrir dagon.ini
* modificar scratch_dir_base a la ruta que se desea (debe ser la misma que FTP_PUBLUSHED_FOLDER)
* Modificar ftp_pub por la ip local, no LOCALHOST. (colocar localhost hace funcionar el transversal, pero provoca errores a la hora de usar los extractores y servicios TPS, preferiblemente usar la ip local)

# Demo de LANDSAT8 con transversal

Los scripts del demo de landsat se encuentran en la carpeta ./WITE/Engines/dagonstar/ y son 2:
* landsat8.py: workflow landsat.
* TPS_landsat.py: workflow post-processing.
* landsat8_and_TPS.py: Las tareas de los workflows anteriores en un mismo script.


Para ejecutar los scripts:
* Ejecutar:
    > python3 -m venv venv
    >
    > . venv/bin/activate
    >
    > pip install -r requieriments.txt
* Para ejecutar landsat8.py
    > python landsat8.py
* Para ejecutar TPS_landsat.py
    > python TPS_landsat.py $PWD
* Para ejecutar landsat8_and_TPS.py
    > python landsat8_and_TPS.py $PWD




# ERRORES
Si se encuentran errores en alguno de los modulos de este sistema, por favor de agregarlos a la lista:

*
*
*
*
*




