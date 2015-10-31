#!/usr/bin/env python

import boto
from boto.s3.key import Key
import h5py
import os
import sys
import uuid

def createBlockFile(fileName):
	"""
	Creates a new HDF5 file named [fileName].
	If a file with that name already exists, it is overwritten.
	Creates a group inside the file called "songs"
	"""
	f = h5py.File(fileName, 'w')
	f.create_group('songs')
	return f

def openBucket(name):
	"""
	Opens the specified S3 bucket.
	Expects to find S3 credentials in environment variables
	"""
	conn = boto.connect_s3()  
	print "Connecting to bucket: {}".format(name)
	bucket = conn.get_bucket(name, validate=True)
	return bucket

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


def packFiles(source, filesPerBlock, dest):
	"""
	Iterates over all files in the directory at [source].
	Packs the contents all h5 files it finds into new h5 files
	containing bundles of [filesPerBlock].
	Uploads those into objects in the S3 bucket named [dest].
	"""
	fileCount = 1
	
	tmpFileName = "tmp.h5"	
	bucket = openBucket(dest)	

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

def printInstructions():
	print "Packs Million Song Subset hdf5 files into bundles and loads them into S3"
	print ""
	print "Usage: packfiles.py [source] [destination] [count]"
	print ""
	print "\tsource: Root directory containing hdf5 files. Will be scanned "
	print "\trecursively."
	print "\tdestination: Name of S3 bucket into which files should be loaded."
	print "\tcount: Number of songs to pack into a single object."
	print ""
	print "Notes:"
	print "The app expects to find AWS credentials in the AWS_ACCESS_KEY_ID and"
	print "AWS_SECRET_ACCESS_KEY environment variables."
	print ""
	print "S3 objects are named using UUIDs."
	print ""
	print "For best results, the destination S3 bucket should be empty. This "
	print "ensures that it's possible to get just the files from this run by "
	print "retrieving all objects in the bucket." 
	print ""
	print "Files are staged in a file called tmp.h5 in the current directory."
	print "This file should normally be cleaned up."
	print ""


def main(argv):
	print ""
	print "packfiles.py"
	print ""

	if len(argv) != 4:
		printInstructions()
		sys.exit()

	sourceDir = argv[1]
	destination = argv[2]
	count = int(argv[3])

	print "Bundling files from {} into batches of {} and uploading them to {}.".format(sourceDir, count, destination)

	packFiles(sourceDir, count, destination)



if __name__ == "__main__": main(sys.argv)