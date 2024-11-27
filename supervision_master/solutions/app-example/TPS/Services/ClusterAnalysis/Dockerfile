FROM r-base:3.6.3
WORKDIR /usr/local/src/stats
RUN apt-get update
RUN apt-get -y install pandoc
RUN apt-get install libcurl4-openssl-dev -y
RUN apt-get install libsodium-dev -y

RUN R -e "install.packages('clusterCrit', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('dbscan', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('plumber')"
RUN R -e "install.packages('dplyr')"

COPY ./stats /usr/local/src/stats

ENTRYPOINT ["Rscript"]
CMD ["init.R"]
