#install.packages("plumber")

library(plumber)
r <- plumb("Graphs.R")  # Where 'plumber.R' is the location of the file shown above
r$run(host="0.0.0.0",port=5500)

