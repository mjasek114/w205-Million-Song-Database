# w205project
Meta Musical Memes workplace

## Packages used
1. h5py: http://www.h5py.org
2. boto: https://github.com/boto/boto

## Useful links
1. Getting the dataset: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
2. Loading HDF5 data into RDDs: https://hdfgroup.org/wp/2015/03/from-hdf5-datasets-to-apache-spark-rdds/
3. MSD sample code: https://github.com/tbertinmahieux/MSongsDB

## TODO:
1. Get up and running with: https://gist.github.com/pbugnion/ea2797393033b54674af

## Getting Started
Instructions for getting packages set up

### Mac

1. It's easiest to use Anaconda to get all the prerequisites intalled: 
  * https://www.continuum.io/downloads
2. Then use it to install the packages listed above:
  * > conda install h5py
  * > conda instal boto
3. Make sure you have your AWS keys stored in the following environment variables:
  * AWS_ACCESS_KEY_ID - Your AWS Access Key ID
  * AWS_SECRET_ACCESS_KEY - Your AWS Secret Access Key
  * Instructions for creating these if you don't already have them http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html 
  * NOTE: DO NOT STORE THESE IN A FILE ANYWHERE INSIDE THE PROJECT DIRECTORY. If you accidentally check them into GitHub, somebody's likely to find them and use them to rack up a very expensive bill.