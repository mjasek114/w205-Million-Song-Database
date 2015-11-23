#!/bin/bash

#yum -y update
yum -y install h5py
yum -y install R
yum -y install r-studio
wget https://download2.rstudio.org/rstudio-server-rhel-0.99.489-x86_64.rpm
yum -y install --nogpgcheck rstudio-server-rhel-0.99.489-x86_64.rpm
yum -y install mysql
yum -y install mysql-server
yum -y install xauth*  #enables ssh-based X11 forwarding for gui apps
yum -y install java-1.7.0-openjdk java-1.7.0-openjdk-devel #necessary for getting hive stuff to start:
service mysqld start

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

