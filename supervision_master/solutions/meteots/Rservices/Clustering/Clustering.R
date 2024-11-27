library(sparcl)
#install.packages('cluster')
library(cluster)
library(ggplot2)

path = "./volumen" #dentro del contenedor
#path = "/home/robot/Escritorio/Projects/Servicios\ web/Diferencial/static" #para pruebas
##################################################################################
avg_sil <- function(df,clusters) {
  ss <- silhouette(clusters, dist(df))
  return (mean(ss[, 3]))
}
##################################################################################
#* @param folder Number of the folder
#* @param K integer
#* @param tipo integer tipo de clustering
#* @param list_values string list of values sepaarated with comma
#* @get /Clustering
ClustHer <- function(folder,K, tipo,list_values){
  K <- as.integer(K)
  Tipo_Clustering = as.integer(tipo)
  list_values <- strsplit(list_values,",")[[1]]
  ###### INICIALIZACION DE VARIABLES ###############
  dataset <- read.csv(paste(path,"/clust/",folder,"/stations.csv",sep = ""), header=FALSE)
   #1 = herarhical , 2= Kmeans, 3 = other
  #############################################

  
  if(Tipo_Clustering==0)
  {
    fechas =unique(dataset$V2)
    datos.etiquetados <- NULL
    plots <- list(1:length(fechas))
    for (f in 1:length(fechas)) {
      data_fecha <- na.omit(dataset[dataset$V2 == levels(fechas)[f],]) ############# PROBANDO EL NA OMIT 
      
      if(length(data_fecha[,1])>2 && length(unique(data_fecha[as.numeric(list_values[1])])[,1] ) >3) {
              # 10 es max dif - 11 es min diff
              values <- NULL
              for (i in as.numeric(list_values)) {
                values <- cbind(values,as.numeric(data_fecha[,as.numeric(i)]))
              }
      
            ##-------------------------------------------------#
            km.sil <- NULL
            hr.sil <- NULL
            Kvalues <- NULL
            perm.out <- HierarchicalSparseCluster.permute(values, wbounds=c(1.5,2:32),nperms=5)
            sparsehc <- HierarchicalSparseCluster(dists=perm.out$dists,wbound=perm.out$bestw, method="average")
            for (k in 2:15){ #recorrer valres de K
              #algoritmos declustering a probar
              if(k<length(data_fecha[,1]) && length(unique(data_fecha[as.numeric(list_values[1])])[,1])> k ){
                
                # si no hay valroes para diferencial
                
                ## KMEANS ##
                km.res <- kmeans(values, centers = k, nstart = 25)
                km.sil <- rbind(km.sil,avg_sil(values,km.res$cluster))
      
                ## HERARHICAL ##
                hr.res <- cutree(sparsehc$hc,k=k)
                hr.sil <- rbind(hr.sil,avg_sil(values,hr.res))
                Kvalues <- k;
              }
            }
            #se obtieenen los maximos y se usa el mejor algoritmo
            max.km <- max(km.sil[2:length(km.sil)]); km.best.k <- max.col(t(km.sil[2:length(km.sil)]))+2
            max.hr <- max(hr.sil[2:length(hr.sil)]); hr.best.k <- max.col(t(hr.sil[2:length(hr.sil)]))+2
            bestCluster <- max.col(cbind(max.hr,max.km)) # 1= herahical 2 = kmeans 3=... 
            
            if(bestCluster==1){ #HERARHICAL
                grupos <- cutree(sparsehc$hc,k=hr.best.k)
                data_fecha <- data.frame(data_fecha,grupos)
              }
            if(bestCluster==2){ #KMEANS
                grupos <- kmeans(values, km.best.k)
                data_fecha <- data.frame(data_fecha,grupos$cluster)
                colnames(data_fecha)[length(data_fecha)] <- "grupos"
            }
            datos.etiquetados <- rbind(datos.etiquetados,data_fecha)
      }
    } #end for de fechas
     
    
  } #-----------------------------------------------------END IF TIPO 0
  if(Tipo_Clustering == 1)
  {
    fechas =unique(dataset$V2)
    datos.etiquetados <- NULL
    for (f in 1:length(fechas)) {
      #CLUSTERING
      data_fecha <- na.omit(dataset[dataset$V2 == levels(fechas)[f],]) ############# PROBANDO EL NA OMIT 
      if(length(data_fecha[,1])>5 && length(unique(data_fecha[as.numeric(list_values[1])])[,1] ) >K ){
        # 10 es max dif - 11 es min diff
        values <- NULL
        for (i in as.numeric(list_values)) {
          print(i)
          values <- cbind(values,as.numeric(data_fecha[,as.numeric(i)]))
        }
        # si no hay valroes para diferencial
        perm.out <- HierarchicalSparseCluster.permute(values, wbounds=c(1.5,2:32),nperms=5)
        sparsehc <- HierarchicalSparseCluster(dists=perm.out$dists,wbound=perm.out$bestw, method="average")
        grupos_sparce <- cbind(cutree(sparsehc$hc,k=K))
        data_fecha <- data.frame(data_fecha,grupos_sparce)
        datos.etiquetados <- rbind(datos.etiquetados,data_fecha)
      }
    }
    
  }
  #FUENTE 2
  if (Tipo_Clustering==2){ #suceptible a errores por los NA
    fechas =unique(dataset$V2)
    datos.etiquetados <- NULL
    for (f in 1:length(fechas)) { # se realiza un clustering por cada fecha
      data_fecha <- na.omit(dataset[dataset$V2 == levels(fechas)[f],])
      if(length(data_fecha[,1])>K){ #si hay masde K registros se realizael clustering
        values <- NULL
        for (i in as.numeric(list_values)) { # se obtienen los valores delas variables a utilizar
          values <- cbind(values,as.numeric(data_fecha[,as.numeric(i)]))
        }
        # si no hay valroes para diferencial
        if (length(unique(data_fecha[as.numeric(list_values[1])])[,1] ) <=K){TempK = 1 
        }else {TempK = K}
        grupos <- kmeans(values,TempK)
        data_fecha <- data.frame(data_fecha,grupos$cluster)
        datos.etiquetados <- rbind(datos.etiquetados,data_fecha)
      }
    }
  }

  ################ escribir el resultado ######################
  ruta = paste(path,"/clust/",folder,"/results.csv",sep = "")
  write.table(datos.etiquetados,ruta,row.names = FALSE,col.names = FALSE , sep = ",")
}



##################################################################################
#* @param folder Number of the folder
#* @param K integer
#* @param list_values string list of values sepaarated with comma
#* @get /ClustImgs
ClustImgs <- function(folder, list_values){
    K <- 0
    list_values <- strsplit(list_values,",")[[1]]
    ###### INICIALIZACION DE VARIABLES ###############
    dataset <- read.csv(paste(path,"/clust/",folder,"/stations.csv",sep = ""), header=FALSE)
  
  fechas =unique(dataset$V2)
  datos.etiquetados <- NULL
  plots <- list(1:length(fechas))
  for (f in 1:length(fechas)) {
    data_fecha <- na.omit(dataset[dataset$V2 == levels(fechas)[f],]) ############# PROBANDO EL NA OMIT 
    if(length(data_fecha[,1])>2 && length(unique(data_fecha[as.numeric(list_values[1])])[,1] ) >3){
      # 10 es max dif - 11 es min diff
      values <- NULL
      for (i in as.numeric(list_values)) {
        values <- cbind(values,as.numeric(data_fecha[,as.numeric(i)]))
      }
      
      ##-------------------------------------------------#
      km.sil <- NULL
      hr.sil <- NULL
      Kvalues <- NULL
      perm.out <- HierarchicalSparseCluster.permute(values, wbounds=c(1.5,2:32),nperms=5)
      sparsehc <- HierarchicalSparseCluster(dists=perm.out$dists,wbound=perm.out$bestw, method="average")
      for (k in 2:15){ #recorrer valres de K
        #algoritmos declustering a probar
        if(k<length(data_fecha[,1]) && length(unique(data_fecha[as.numeric(list_values[1])])[,1] ) >k){
          ## KMEANS ##
          km.res <- kmeans(values, centers = k, nstart = 25)
          km.sil <- rbind(km.sil,avg_sil(values,km.res$cluster))
          
          ## HERARHICAL ##
          hr.res <- cutree(sparsehc$hc,k=k)
          hr.sil <- rbind(hr.sil,avg_sil(values,hr.res))
          Kvalues <- k;
        }
      }
      #se obtieenen los maximos y se usa el mejor algoritmo
      max.km <- max(km.sil[2:length(km.sil)]); km.best.k <- max.col(t(km.sil[2:length(km.sil)]))+2
      max.hr <- max(hr.sil[2:length(hr.sil)]); hr.best.k <- max.col(t(hr.sil[2:length(hr.sil)]))+2
      bestCluster <- max.col(cbind(max.hr,max.km)) # 1= herahical 2 = kmeans 3=... 
      
      if(bestCluster==1){ #HERARHICAL
        best="HER"
        bestV=hr.best.k
        grupos <- cutree(sparsehc$hc,k=hr.best.k)
        data_fecha <- data.frame(data_fecha,grupos)
      }
      if(bestCluster==2){ #KMEANS
        best="KMEANS"
        bestV=km.best.k
        grupos <- kmeans(values, km.best.k)
        data_fecha <- data.frame(data_fecha,grupos$cluster)
        colnames(data_fecha)[length(data_fecha)] <- "grupos"
      }
      # GENERAR GRAFICA DE LA SILUETA
      Data_plot <- as.data.frame(cbind(km.sil,hr.sil,2:Kvalues))
      colnames(Data_plot) <-c("Km","Hr","K")
      kmpoints <- as.data.frame(cbind(km.best.k,max.km))
      hrpoints <- as.data.frame(cbind(hr.best.k,max.hr))
      
      plots[[f]] <- ggplot(Data_plot, aes(x=K,group=1)) +
        geom_line(aes(y=Km, colour = "Kmeans") )+
        geom_line(aes(y=Hr, colour = "Herarhical"))+
        geom_point(aes(y=Km))+
        geom_point(aes(y=Hr))+
        geom_point(data=kmpoints, mapping=aes(x=km.best.k, y=max.km),colour="red" )+
        geom_point(data=hrpoints, mapping=aes(x=hr.best.k, y=max.hr),colour="red" )+
        ylab("Silhouette average")+
        xlab("Numberof groups (K)")+
        labs(title = paste( "Silhouette ",fechas[f],": ",best," - ",bestV) )
      
      date.today = as.Date(levels(fechas)[f],format='%d/%m/%Y')
      png(paste(path,"/clust/",folder,"/",date.today,"_Sil.png",sep = ""),width = 10, height = 10, units='cm', res = 100)
      paste(path,"/clust/",folder,"/results.csv",sep = "")
      print(plots[[f]])
      dev.off()
      datos.etiquetados <- rbind(datos.etiquetados,data_fecha)
    }
  } #end for de fechas
}