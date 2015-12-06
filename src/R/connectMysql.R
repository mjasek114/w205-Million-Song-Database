install.packages("DBI")
library(DBI)
install.packages("RMySQL")
library(RMySQL)

#load a driver for a MySQL-type database
drv = dbDriver("MySQL")

#create a connectino to the database
con = dbConnect(drv, user="metamusic", password="", dbname="songs", host="localhost")

# list tables or fields
dbListTables(con)
dbListFields(con, 'song')

#create a results set that is still not yet downloaded in to R
rs = dbSendQuery(con, "select * from song")

#get the results set and create and load a dataframe in R
df = fetch(rs, n=-1)