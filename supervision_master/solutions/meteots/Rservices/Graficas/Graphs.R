library(ggplot2)
library(future)
#####################################################################
path = "./volumen" #dentro del contenedor
#path = "../../static" #para pruebas
#####################################################################


Mode <- function(x, na.rm = FALSE) {
  if(na.rm){
    x = x[!is.na(x)]
  }
  ux <- unique(x)
  return(ux[which.max(tabulate(match(x, ux)))])
}

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


##################################################################################
#* @param folder Number of the folder
#* @get /dates
general <- function(folder){
  emas.data <- read.csv(paste(path,"/plots/",folder,"/emas.csv",sep = ""), header=FALSE)
  merra.data <- read.csv(paste(path,"/plots/",folder,"/merra.csv",sep = ""), header=FALSE)
  
  fechas =unique(emas.data$V2)
  ######################################
  # STADISTICS
  emas <- emas.data
  stations.emas =unique(emas$V5)
  fecha.emas =unique(emas$V2)
  merra <- merra.data
  
  me = 1:length(stations.emas)
  emas.medians = as.data.frame(cbind(me,me))
  emas.modas = as.data.frame(cbind(me,me))
  emas.medias = as.data.frame(cbind(me,me,me,me,me))
  emas.desv = as.data.frame(cbind(me,me))
  merra.medias = as.data.frame(cbind(me,me))
  emas = as.data.frame(emas)
  
  merra = as.data.frame(merra)
  
  emas$V6 = replace(emas$V6,emas$V6=='Null',NA )
  emas$V6 = as.numeric(emas$V6)
  merra$V7 = as.numeric(merra$V7)
  
  #variables de plots
  plots <- list(1:length(fecha.emas))
  boxplots <- list(1:length(fecha.emas))
  stations.plots <- list(1:length(stations.emas))
  fechas.nombres.plot = NULL
  fechas.nombres.box =NULL 
  for (j in 1:length(fecha.emas)) { # FECHAS ---------------------------------
    merra.today = merra[merra$V2==levels(fecha.emas)[j],]
    if(length(merra.today[,1])>1){ #si hay datos de merra
      for (i in 1:length(stations.emas)) {
        dat.today <- emas[emas$V2==fecha.emas[j],]
        emas.medians[i,1]= as.numeric(median(dat.today$V6[dat.today$V5==levels(stations.emas)[i]]),na.rm=TRUE)
        emas.medians[i,2]= levels(stations.emas)[stations.emas[i]]
        emas.modas[i,1]= Mode(dat.today$V6[(dat.today$V5==levels(stations.emas)[i])] , na.rm=TRUE )
        emas.modas[i,2]= levels(stations.emas)[stations.emas[i]]
        emas.medias[i,1] = mean(as.numeric(dat.today$V6[(dat.today$V5==levels(stations.emas)[i])]) ,na.rm = TRUE)
        emas.medias[i,1] <- replace(emas.medias[i,1], is.nan(emas.medias[i,1]),NA ) #remplazar ? con NA 
        emas.medias[i,2] = sd(dat.today$V6[(dat.today$V5==levels(stations.emas)[i])],na.rm = TRUE)
        emas.medias[i,3] = levels(stations.emas)[stations.emas[i]]
        #emas.medias[i,4] = max(dat.today$V6[(dat.today$V5==levels(stations.emas)[i])])
        #emas.medias[i,5] = min(dat.today$V6[(dat.today$V5==levels(stations.emas)[i])])
        
        #merra
        if (length(merra.today$V7[merra.today$V1 ==levels(stations.emas)[i]])==0 ){
          merra.medias[i,1] <- NA
          merra.medias[i,2] = levels(stations.emas)[stations.emas[i]]
        }
        else{
          merra.medias[i,1] = as.numeric(merra.today$V7[merra.today$V1 ==levels(stations.emas)[i]])
          merra.medias[i,2] = levels(stations.emas)[stations.emas[i]]
        }
      }
      #ordenamiento para priemrea grafica
      plot.moda = as.data.frame(cbind(
        sort(emas.medians[,1],na.last = FALSE), 
        sort(emas.modas[,1],na.last = FALSE),
        sort(emas.medias[,1],na.last = FALSE),
        as.numeric(emas.medias[,2]),
        sort(merra.medias[,1],na.last = FALSE),
        1:length(sort(emas.medians[,1],na.last = FALSE)) ))
      
      for (p in 1:length(plot.moda[,1])) {
        plot.moda[p,4] <- sort(emas.medias[emas.medias[,1]==plot.moda[p,3] ,2])[1]
      }
      #ordenamiento para segunda grafica
      
      
      pd <- position_dodge(0.1)
      plots[[j]] <- ggplot(data=plot.moda, aes(x=V6,group=1)) +
        geom_line(aes(y=V1, colour = "median - Emas") )+
        geom_line(aes(y=V2, colour = "mode - Emas"))+
        geom_line(aes(y=V3, colour = "mean - Emas"))+
        geom_line(aes(y=V5, colour = "mean - Merra"))+
        geom_errorbar(aes(ymin=V3-V4, ymax=V3+V4), width=.1,position=pd) +
        ylab("Temperature (C°)")+
        xlab("Stations ordered")+
        labs(title = paste( "Temperature trends",levels(fecha.emas)[j]) )
      boxplots[[j]] <- ggplot(dat.today, aes(x=V5, y=V6,colour="Emas")) + 
        geom_boxplot() +
        stat_summary(fun.y=mean, geom="point", shape=23, size=4)+
        geom_line(data=merra.today,aes(x=V1, y=V7,group=2,colour="MERRA - Mean"))+
        geom_point(data=merra.today, aes(x=V1,y=V7,group=2 ),colour="blue" )+
        geom_line(data=merra.today,aes(x=V1, y=V6,group=1,colour="MAX-MIN MERRA" ))+
        geom_point(data=merra.today,aes(x=V1,y=V6,group=1,colour="MAX-MIN MERRA"),colour="orange" )+
        geom_line(data=merra.today,aes(x=V1, y=V5,group=1,colour="MAX-MIN MERRA"))+
        geom_point(data=merra.today,aes(x=V1,y=V5,group=1,colour="MAX-MIN MERRA"), colour="orange" )+
        scale_color_brewer(palette="Dark2")+
        ylab("Temperature (C°)")+
        xlab("Meteorological station")+
        labs(title = paste( "EMAS and MERRA temperature by Meteorological station\n",levels(fecha.emas)[j]) )+
        theme(legend.title = element_blank())
      
        fechas.nombres.plot = rbind(fechas.nombres.plot,levels(fecha.emas)[j])
    } ## fin del if para validar que tenga datos de esa fecha
    else
    {
      boxplots[[j]] <- 0
    }
    
  } #end of for
  
  
  ############ GUARDAR GRAFICOS ################
  # plots por estaciones
  plan(multiprocess)
  
  porc1%<-%{
    for (x in 1:length(plots) ) {
      dte = fechas.nombres.plot
      date.today = as.Date(dte[x],format='%d/%m/%Y')
      png(paste(path,"/plots/",folder,"/",date.today,"_hist.png",sep = ""),width = 20, height = 20, units='cm', res = 100)
      print(plots[[x]])
      dev.off()
    }
  }
  porc2%<-%{
    for (x in 1:length(plots) ) {
      if(is.list(boxplots[[x]])){
        dte = fechas.nombres.plot
        date.today = as.Date(dte[x],format='%d/%m/%Y')
        png(paste(path,"/plots/",folder,"/",date.today,"_box.png",sep = ""),width = 28, height = 20, units='cm', res = 100)
        print(boxplots[[x]])
        dev.off() 
      }
    }
  }
  porc1
  porc2
}




#########################################################################
#* @param folder Number of groups
#* @get /stations
stat <- function(folder){
  emas.data <- read.csv(paste(path,"/plots/",folder,"/emas.csv",sep = ""), header=FALSE)
  
  emas <- emas.data
  stations.emas =unique(emas$V5)
  fecha.emas =unique(emas$V2)
  
  plan(multiprocess)
  
  porc1%<-%{
    for (i in 1:round(length(stations.emas)/2)) {
      tmp.data <- as.data.frame(emas[emas$V5==levels(stations.emas)[i],])
      tmp.data$V7 <- as.numeric(as.character(tmp.data$V7)) 
      p1 <- ggplot(data=tmp.data, aes(x=V11, y=V6,colour=V2,group=V2) )+
        geom_line()+ geom_point()+
        ylab("Temperature (C°)")+
        xlab("Time of the day")+
        labs(title = paste( "EMAS temperature by hour - ",tmp.data$V1[1]) )+
        theme(legend.title = element_blank(),legend.position="none")
      
      p2 <- ggplot(data=tmp.data, aes(x=V11, y=V7,colour=V2,group=V2) )+
        geom_line()+ geom_point()+
        ylab("humidity (%)")+
        xlab("Time of the day")+
        labs(title = paste( "EMAS humidity by hour - ",tmp.data$V1[1]) )+
        theme(legend.title = element_blank())
      
      jpeg(paste(path,"/plots/",folder,"/",tmp.data$V5[1],".jpeg",sep = ""),width = 28, height = 20, units='cm', res = 100)
      print(multiplot(p1,p2,cols = 1))
      dev.off()
      
    }
  }
  porc2%<-%{
    for (i in (round(length(stations.emas)/2)+1):length(stations.emas)) {
      tmp.data <- as.data.frame(emas[emas$V5==levels(stations.emas)[i],])
      tmp.data$V7 <- as.numeric(as.character(tmp.data$V7)) 
      p1 <- ggplot(data=tmp.data, aes(x=V11, y=V6,colour=V2,group=V2) )+
        geom_line()+ geom_point()+
        ylab("Temperature (C°)")+
        xlab("Time of the day")+
        labs(title = paste( "EMAS temperature by hour - ",tmp.data$V1[1]) )+
        theme(legend.title = element_blank(),legend.position="none")
      
      p2 <- ggplot(data=tmp.data, aes(x=V11, y=V7,colour=V2,group=V2) )+
        geom_line()+ geom_point()+
        ylab("humidity (%)")+
        xlab("Time of the day")+
        labs(title = paste( "EMAS humidity by hour - ",tmp.data$V1[1]) )+
        theme(legend.title = element_blank())
      
      jpeg(paste(path,"/plots/",folder,"/",tmp.data$V5[1],".jpeg",sep = ""),width = 28, height = 20, units='cm', res = 100)
      print(multiplot(p1,p2,cols = 1))
      dev.off()
      
    }
  }
  
  porc1
  porc2

}

