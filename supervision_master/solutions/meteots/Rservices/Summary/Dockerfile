FROM r-base
COPY ./stats /usr/local/src/stats
WORKDIR /usr/local/src/stats
RUN apt-get update
RUN apt-get -y install pandoc
RUN R -e "install.packages('plumber')"
RUN R -e "install.packages('jsonlite')"
RUN R -e "install.packages('rmarkdown')"
RUN R -e "install.packages('dplyr')"
ENTRYPOINT ["Rscript"]
CMD ["init.R"]