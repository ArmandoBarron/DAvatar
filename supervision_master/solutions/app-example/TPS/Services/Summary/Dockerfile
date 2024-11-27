FROM r-base:3.6.3
WORKDIR /usr/local/src/stats
RUN apt-get update && apt-get install -y build-essential
RUN apt-get -y install pandoc
RUN apt-get install libcurl4-openssl-dev -y
RUN apt-get install libsodium-dev -y

RUN R -e "install.packages('plumber')"
RUN R -e "install.packages('jsonlite')"
RUN R -e "install.packages('rmarkdown')"
RUN R -e "install.packages('dplyr')"

COPY ./stats /usr/local/src/stats

ENTRYPOINT ["Rscript"]
CMD ["init.R"]