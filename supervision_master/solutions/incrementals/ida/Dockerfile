FROM fbalderas/ida:base

RUN pip install numpy --user

#Se copia el Codigo de las Aplicaciones a la imagen de contenedor
COPY ./Code/ /home/Code/
# RUN chmod -R 777 /home/Code/ .

WORKDIR /home/Code/