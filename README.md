# Meta Musical Memes - W205 Fall 2015

## Overview
For several decade, music fans have been referring to many kinds of pop music particularly the extremely popular songs as “formulaic.” This is usually meant to be a negative term, but it causes those of a certain disposition (Berkeley Data Science students) to wonder if we can actually articulate the “formula” or at least give a corpus of data to songwriters and music producers which helps assess the commercial potential for some work.

## Scope
The scope of this project was to create a model of a common big data architecture and demonstrate its usefulness by creating a prototype. The general architecture consists of ingesting data, processing it, storing it for analysis and analyzing it. The prototype illustrates the following:
* Ingest data. Ingest musical data from 3 sources listed below (Python).
* Load data. Load data to a temporary location for processing (Amazon S3).
* Transform data. Clean and transform data into a useable format (Hive).
* Store data for processing. Load merged data into a relational database (MySQL).
* Process data: Analyze data to accomplish business objective (RStudio Server, Shiny Server).

The Million Song Dataset (MSD) is a body of data created by LabROSA at Columbia University, and provided to the public via a public Amazon Public Dataset . It primarily consists of the data that The Echo Nest publishes for 1,000,000 songs. This data was processed, cleaned, and joined with Billboard chart data and authorship data from the American Society of Composers, Authors and Publishers (ASCAP), then analyzed in various ways which would be interesting to the general population of music fans as well as music industry professionals.

## Documentation
1. https://github.com/mjasek114/w205-Million-Song-Database/blob/master/MetaMusicalMemes_FinalPresentation.pdf
2. https://github.com/mjasek114/w205-Million-Song-Database/blob/master/MetaMusicalMemes_FinalReport.pdf

## Packages used
1. h5py: http://www.h5py.org
2. boto: https://github.com/boto/boto

## Useful links
1. Getting the dataset: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
2. Loading HDF5 data into RDDs: https://hdfgroup.org/wp/2015/03/from-hdf5-datasets-to-apache-spark-rdds/
3. MSD sample code: https://github.com/tbertinmahieux/MSongsDB

## Getting Started
Instructions for getting packages set up

1. Spin up an m3.medium AWS server with the image ami-003f7f6a
	* Ensure you have the following ports open: 8787, 3838
2. Login to the server via the command line
3. Execute the following (replace your values for things in {braces}):

cd /data

git init

git clone https://{yourGithubUsername}@github.com/SeanU/w205project.git

cd w205project

export AWS_ACCESS_KEY_ID={yourkeyID}

export AWS_SECRET_ACCESS_KEY={yourkey}

export AWS_DEFAULT_REGION=us-east-1

bash setup-scripts/install-packages.sh # Get some coffee--this takes about half an hour

  * Instructions for creating AWS access keys if you don't already have them 
http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html
 
  * NOTE: DO NOT STORE THESE IN A FILE ANYWHERE INSIDE THE PROJECT DIRECTORY. If you accidentally check them into GitHub, somebody's likely to find them and use them to rack up a very expensive bill.

4. Navigate your browser to {yourInstanceIP}:3838 For the Shiny server
5. Navigate your browser to {yourInstanceIP}:8787 For RStudio

