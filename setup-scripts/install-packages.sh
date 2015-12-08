#!/bin/bash

#yum -y update
yum -y install h5py
yum -y install R
yum -y install r-studio
wget https://download2.rstudio.org/rstudio-server-rhel-0.99.489-x86_64.rpm
yum -y install --nogpgcheck rstudio-server-rhel-0.99.489-x86_64.rpm
sudo rstudio-server stop
sudo rstudio-server start
yum -y install mysql
yum -y install mysql-server
yum -y install mysql-devel
yum -y install xauth*  #enables ssh-based X11 forwarding for gui apps
yum -y install java-1.7.0-openjdk java-1.7.0-openjdk-devel #necessary for getting hive stuff to start:
service mysqld start

# Rstudio stuff and shiny stuff won't work under
# the metamusic user w/o access to /tmp
chmod 777 /tmp

# AWS CLI Tools
pip install awscli

# Adjust environment variables
export SPARK_HOME=/home/dan/spark15

# Make a generic user
useradd metamusic
#su metamusic
sudo -u metamusic mkdir /home/metamusic/src

# Install Anaconda, which has all necessary scientific python libraries built in
cd /home/metamusic/src
sudo -u metamusic wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.0-Linux-x86_64.sh
sudo -u metamusic bash Anaconda2-2.4.0-Linux-x86_64.sh -b  #-b is batch mode-->no user interaction required

# Install the mysql interface inside Anaconda
sudo -u metamusic /home/metamusic/anaconda2/bin/conda install -y mysql-python
#sys.path.append('/data/W205_Final/w205project/src/')

# Install Shiny Server
# After you install Shiny Server, the shiny-server process will be started
R -e "install.packages('DBI', repos='http://cran.rstudio.com/')"
R -e "install.packages('RMySQL', repos='http://cran.rstudio.com/')"
R -e "install.packages('ggplot2', repos='http://cran.rstudio.com/')"
R -e "install.packages('shiny', repos='http://cran.rstudio.com/')"
R -e "library(DBI)"
R -e "library(RMySQL)"
R -e "library(ggplot2)"
R -e "library(shiny)"
wget https://download3.rstudio.org/centos5.9/x86_64/shiny-server-1.4.0.718-rh5-x86_64.rpm
yum install -y --nogpgcheck shiny-server-1.4.0.718-rh5-x86_64.rpm
mv /srv/shiny-server/index.html /srv/shiny-server/index.html~


