#FROM r-base:3.6.3
#WORKDIR /usr/local/src/stats
#RUN apt-get update
#RUN apt-get -y install pandoc
#RUN apt-get install libcurl4-openssl-dev -y
#RUN apt-get install libsodium-dev -y

FROM r-base:4.4.0
RUN apt-get update --allow-unauthenticated --allow-insecure-repositories
RUN apt-get -y --allow-unauthenticated install usrmerge   # Instala el paquete usrmerge
RUN apt-get -y --allow-unauthenticated install pandoc -o APT::Immediate-Configure=0 
RUN apt-get -y --allow-unauthenticated install libsodium-dev
RUN apt-get install -y --allow-unauthenticated git-core \   
    libssl-dev \   
    libcurl4-gnutls-dev

RUN R -e "install.packages('clusterCrit', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('dbscan', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('plumber')"
RUN R -e "install.packages('dplyr')"

COPY ./stats /usr/local/src/stats

ENTRYPOINT ["Rscript"]
CMD ["init.R"]
