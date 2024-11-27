# Genera una imagen de contenedor de un Kulla Block que contiene el patrón Master/slave
# desarrollado usando el modelo de programación Kulla
# Creador: Hugo German Reyes Anastacio
# Mail: hugo.reyes@cinvestav.mx
# Se indica la imagen de contenedor que contiene las dependencias de software de Kulla
FROM hgreyesa/ssl
# Se copian los binarios de las aplicaciones desarrolladas así como las bibliotecas que estas aplicaciones utilizan
COPY MasterSlave/ /home/MasterSlave/
WORKDIR /home/MasterSlave/
RUN make

# Para construir esta imagen usar el comando
# docker build -f Dockerfile -t hgreyesa/masterslave .
#-->docker build: indica que se realizará una construcción de imagen de contenedor
#-->-f: indica que se usará un archivo Dockerfile que tiene un nombre distinto al nombre por defecto "Dockerfile"
#-->Dockerfile: es el nombre del archivo dockerfile que será usado para crear la imagen de contenedor
#--> -t: indica que se le asignará un nombre a la imagen de contenedor
#--> hgreyesa/masterslave Es el nombre que se le asignará a la imagen de contenedor
#--> . Indica el fin del comando