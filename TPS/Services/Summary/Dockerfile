FROM r-base:4.4.0

RUN apt-get update --allow-unauthenticated --allow-insecure-repositories
RUN apt-get -y --allow-unauthenticated install usrmerge   # Instala el paquete usrmerge
RUN apt-get -y --allow-unauthenticated install pandoc -o APT::Immediate-Configure=0 
RUN apt-get -y --allow-unauthenticated install libsodium-dev
RUN apt-get install -y --allow-unauthenticated git-core \   
    libssl-dev \   
    libcurl4-gnutls-dev

RUN R -e "install.packages('jsonlite')"
RUN R -e "install.packages('rmarkdown')"
RUN R -e "install.packages('dplyr')"
RUN R -e "install.packages('plumber', repos='https://cloud.r-project.org/')"

COPY ./stats /usr/local/src/stats
WORKDIR /usr/local/src/stats

ENTRYPOINT ["Rscript"]
CMD ["init.R"]
