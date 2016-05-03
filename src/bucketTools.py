# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 08:18:51 2015

@author: james
"""
import boto
from boto.s3.key import Key
import uuid



def openBucket(name):
    """
    Opens the specified S3 bucket.
    Expects to find S3 credentials in environment variables

    in BASH:
    export AWS_ACCESS_KEY_ID= ...
    export AWS_SECRET_ACCESS_KEY=...
    export AWS_DEFAULT_REGION=us-east-1

 
    """
    conn = boto.connect_s3()  
    print "Connecting to bucket: {}".format(name)
    bucket = conn.get_bucket(name, validate=True)
    return bucket
    
    
def getFileKeys(bucket):
    keyz = bucket.list()
    
def upload(filename, bucket):
    """
    Uploads the specified file to an S3 bucket.
    Object's key will be a UUID.
    """
    k = Key(bucket)
    k.key = uuid.uuid1().hex
    print "Uploading batch to {}, key: {}...".format(bucket.name, k.key)
    k.set_contents_from_filename(filename, reduced_redundancy=True)
    print "  Done."
     


    bucket = openBucket(dest)	
 
 
def packFiles(source, filesPerBlock, dest):
	"""
	Iterates over all files in the directory at [source].
	Packs the contents all h5 files it finds into new h5 files
	containing bundles of [filesPerBlock].
	Uploads those into objects in the S3 bucket named [dest].
	"""
	fileCount = 1
	
	tmpFileName = "tmp.h5"	


	outFile = createBlockFile(tmpFileName)	
	for dirname, subdirs, files in os.walk(source):	
	    print 'Scanning ' + dirname + '...'	
	    for f in files:	
	        if f.endswith('.h5'):	
	            inFile = h5py.File(os.path.join(dirname, f), 'r')	
	            outFile.copy(inFile, outFile['songs'], f)	
	            inFile.close()	
	            fileCount = fileCount + 1	
	        if(fileCount > filesPerBlock):	
	            outFile.close()	
	            upload(tmpFileName, bucket)	
	            fileCount = 1	
	            outFile = createBlockFile(tmpFileName)	

   	outFile.close()
   	if fileCount > 1:
	   	upload(tmpFileName, bucket)

	os.remove(tmpFileName)
