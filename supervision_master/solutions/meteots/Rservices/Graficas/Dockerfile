FROM trestletech/plumber
WORKDIR home
RUN mkdir volumen

RUN Rscript -e 'install.packages("ggplot2")'
RUN Rscript -e 'install.packages("future")'

COPY ./Graphs.R Graphs.R
COPY ./server.R server.R

ENTRYPOINT ["Rscript"]
CMD ["server.R"]
