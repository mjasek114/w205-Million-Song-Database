#!/bin/bash

#install R
yum install -y R

#install RStudio-Server
wget https://download2.rstudio.org/rstudio-server-rhel-0.99.465-x86_64.rpm
yum install -y --nogpgcheck rstudio-server-rhel-0.99.465-x86_64.rpm

#install shiny and shiny-server
R -e "install.packages('shiny', repos='http://cran.rstudio.com/')"
R -e "install.packages('RCurl')"
R -e "library(RCurl)
wget https://download3.rstudio.org/centos5.9/x86_64/shiny-server-1.4.0.718-rh5-x86_64.rpm
yum install -y --nogpgcheck shiny-server-1.4.0.718-rh5-x86_64.rpm
#To use Shiny Server, you have to make some small configuration changes.
sudo /opt/shiny-server/bin/deploy-example user-dirs
mkdir ~/ShinyApps

#add user(s)
#useradd username
#echo username:password | chpasswd

sudo yum install curl-devel

#install other r packages that you need here

#stop R Studio Server if it is running and restart it
rstudio-server stop
rstudio-server start

#on your AWS ec2 instance make Inbound Custom TCP Rules that open ports 8787 for
#R Studio and 
#http://ec2-YOUR-IP.REGION.compute.amazonaws.com:8787
#http:// ec2-YOUR-IP.REGION.compute.amazonaws.com:3838/<your_username>/MyApp
