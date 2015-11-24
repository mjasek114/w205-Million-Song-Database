"""
author: Megan Jasek
"""

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.connection import Location
import os
import sys
import uuid

def getS3File(bucketName, localStorePath):
    '''
    Get the contents of the S3 object with key localStorePath in the S3 bucket called
    bucketName.  Write these contents to a file called localStorePath.
    
    Expects to find AWS credentials in the AWS_ACCESS_KEY_ID 
    and AWS_SECRET_ACCESS_KEY environment variables
    '''
    # expects to find AWS credentials in the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
    # create a connection to s3
    c = boto.connect_s3()
    # get the bucket that you want to access
    b = c.get_bucket(bucketName, validate = True)
    # get the key from the named bucket
    key = b.get_key(localStorePath)
    # takes the contents of the object you found above and writes them to the file called localStorePath
    key.get_contents_to_filename(localStorePath)
    
def putS3File(localPath, bucketName):
    '''
    Writes the file named localPath to a new S3 object in the S3 bucket called bucketName.
    Sets permissions for the new S3 object for team members.  
    
    Expects to find AWS credentials in the AWS_ACCESS_KEY_ID 
    and AWS_SECRET_ACCESS_KEY environment variables
    '''
    # expects to find AWS credentials in the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
    # create a connection to s3
    c = boto.connect_s3()
    # get the bucket that you want to access
    b = c.get_bucket(bucketName)
    # create a generic Key object to use with this bucket
    k = Key(b)
    # finds the object within the bucket with an ID (or key) of localPath
    k.key = localPath
    # sets the contents of the new object to the contents of the file named localPath
    k.set_contents_from_filename(localPath, reduced_redundancy=True)
    # add permistions for team members
    k.add_email_grant('READ', 'megan@alum.mit.edu')
    k.add_email_grant('READ', 'seanu@ischool.berkeley.edu')
    k.add_email_grant('READ', 'james.king@berkeley.edu')

#test functions
#putS3File('Billboardkeys.xls', 'megantestbucketforiamrole')
#getS3File('megantestbucketforiamrole','Billboardkeys.xls')
