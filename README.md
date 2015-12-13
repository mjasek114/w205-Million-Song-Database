# w205project
Meta Musical Memes workplace

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
3. Execute the following (replace your values for things in {braces}:

cd /data

git init

git clone https://{yourGithubUsername}@github.com/SeanU/w205project.git

cd w205project

export AWS_ACCESS_KEY_ID={yourkeyID}

export AWS_SECRET_ACCESS_KEY={yourkey}

export AWS_DEFAULT_REGION=us-east-1

bash setup-scripts/install-packages.sh # Get some coffee--this takes a while

  * Instructions for creating AWS access keys if you don't already have them http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html
 
  * NOTE: DO NOT STORE THESE IN A FILE ANYWHERE INSIDE THE PROJECT DIRECTORY. If you accidentally check them into GitHub, somebody's likely to find them and use them to rack up a very expensive bill.



