FROM trestletech/plumber
WORKDIR home
RUN mkdir volumen

RUN Rscript -e 'install.packages("sparcl")'
RUN Rscript -e 'install.packages("glue")'
RUN Rscript -e 'install.packages("ggplot2")'
RUN Rscript -e 'install.packages("cluster")'



COPY ./Clustering.R Clustering.R
COPY ./server.R server.R

ENTRYPOINT ["Rscript"]
CMD ["server.R"]
