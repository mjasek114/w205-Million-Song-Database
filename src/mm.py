# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:22:50 2015

@author: james
"""

# Modules needed below:
#   Pandas
#   h5py
#   psycopg2
#   MySQL-python
#   sqlalchemy

       
import os
import os.path
#import h5py
#import sys
#import sqlalchemy as sql
import boto
from boto.s3.key import Key
    
#==============================================================================================================#
#==============================================================================================================#    
    
def listS3Files(bucketName='w205-msd', verbose = True):
        """
        Opens the specified S3 bucket.
        Expects to find S3 credentials in environment variables
        
        in BASH:
            export AWS_ACCESS_KEY_ID= ...
            export AWS_SECRET_ACCESS_KEY=...
            export AWS_DEFAULT_REGION=us-east-1

 
        """
        conn = boto.connect_s3()  
        if verbose:
            print "Fetching filenames for bucket: ", bucketName
            
        bucket = conn.get_bucket(bucketName, validate=True)
        
        bucketKeys = [thisKey for thisKey in bucket.list()]
        
        return bucketKeys                         

#==============================================================================================================#    

def getS3File(remoteKey, localStorePath, verbose = True):
    '''
    Places the file pointed to by remoteKey in the localStorePath folder
    with the name remoteKey.name.
    
    Expects to find AWS credentials in the AWS_ACCESS_KEY_ID and 
    AWS_SECRET_ACCESS_KEY environment variables

    '''

    if verbose:
        print "Writing file ", os.path.join(localStorePath,remoteKey.name)

    # takes the contents of the object you found above and writes them to the file called localStorePath
    remoteKey.get_contents_to_filename(os.path.join(localStorePath,remoteKey.name))
 
#==============================================================================================================#    

def putS3File(localPath, bucketName):
    '''
    Writes the file named in localPath to the S3 bucket called bucketName.    
    
    Expects to find AWS credentials in the AWS_ACCESS_KEY_ID 
    and AWS_SECRET_ACCESS_KEY environment variables
    '''
   # create a connection to s3
    connection = boto.connect_s3()

    # get the bucket that you want to access
    bucket = connection.get_bucket(bucketName)

    # create a generic Key object to use with this bucket
    k = Key(bucket)

    # finds the object within the bucket with an ID (or key) of localPath
    k.key = localPath
    
    # sets the contents of the new object to the contents of the file named localPath
    k.set_contents_from_filename(localPath, reduced_redundancy=True)
    
    # adds read access for all of us.  all users must be AWS users
    k.add_email_grant('READ', 'megan@alum.mit.edu')
    k.add_email_grant('READ', 'seanu@ischool.berkeley.edu')
    k.add_email_grant('READ', 'james.king@berkeley.edu')

#==============================================================================================================#

def nodeToDict(bucketKey, verbose = True, refresh=False):
    '''
    This function is intended for use in a parallel processing map.
    Inputs a bucket key, downloads the data, and extracts some important info 
    
    Returns a list of dictionaries, each dictionary has all "analysis" fields in the song.
    It's possible that all songs don't have exactly the same fields.
    
    Note: This code expects to find an extra field called localStorePath
    in the key object.   Implementing this way enables parallel processing.
    '''
    import h5py
    import os
    import os.path

    if not hasattr(bucketKey, 'localStorePath'):
        bucketKey.localStorePath = '~'
        
    songInfo = []
    
    
    # don't reprocess files
    downloadedFiles = os.listdir(bucketKey.localStorePath)
        
    if bucketKey.name in downloadedFiles:
        print 'We seem to already have the file ', bucketKey.name, '. Verifying size'
        
        localFileSize = os.path.getsize(os.path.join(bucketKey.localStorePath, bucketKey.name))

        if (bucketKey.size == localFileSize) and (refresh==False):
            print 'Skipping download--going straight to processing'
            
        else:
    
            try:
                if verbose:
                    print 'Fetching data file ', bucketKey, ' from bucket ', bucketKey.bucket, '.  Size: ', bucketKey.size
                getS3File(bucketKey, bucketKey.localStorePath)
            except:
                print 'Error fetching file ', bucketKey
                return []
        
    try:    
        if verbose:
            print 'Processing ', bucketKey
        
        thisH5File = h5py.File(os.path.join(bucketKey.localStorePath,bucketKey.name))
        thisBlockSongList = thisH5File['songs']
                
        for thisSong in thisBlockSongList:
            # There are 3 categories of data in this set.  Grab stuff from all
            # of them
            analysisDataSet = thisH5File['songs'][thisSong]['analysis']['songs']
            metadataDataSet = thisH5File['songs'][thisSong]['metadata']['songs']
            musicbrainzDataSet = thisH5File['songs'][thisSong]['musicbrainz']['songs']
        
            outDict = dict()
        
            for measurement1 in analysisDataSet.dtype.names:
                value = analysisDataSet[measurement1][0]
                
                if len(str(value)) > 0:
                    outDict[measurement1] = value
                else:
                    outDict[measurement1] = 'NA'
        
                
        
            for measurement2 in musicbrainzDataSet.dtype.names:
                value = musicbrainzDataSet[measurement2][0]
        
                if len(str(value)) > 0:
                    outDict[measurement2] = value
                else:
                    outDict[measurement2] = 'NA'
        
        
            for measurement3 in metadataDataSet.dtype.names:
                value = metadataDataSet[measurement3][0]            ##
        
                if len(str(value)) > 0:
                    outDict[measurement3] = value
                else:
                    outDict[measurement3] = 'NA'
                
            songInfo.append(outDict)

    except:
        print 'Error loading file ', bucketKey
    
    return songInfo #list of dictionaries
    
#==============================================================================================================#
#==============================================================================================================#

class metaMusic:
    
    def __init__(self, minPartitions = 4, filesPerBlock = 100, verbose = True):

        if verbose:
            print 'Setting up project folders.'
            
        self.verbose = verbose
        self.mainRoot = '/data/W205_Final/w205project/'
        self.mssRoot = '/data/W205_Final/w205project/data/'
        self.blocksRoot = '/data/W205_Final/w205project/blocks/'
        self.resultsRoot = '/data/W205_Final/w205project/resultsRoot/'
        self.results = None  # This is for holding the extraction results in memory
        self.filesPerBlock = filesPerBlock  # Gives about 30MB/file. Should use larger size in production.    
        self.minPartitions = minPartitions  #minimum number of partitions multiprocessing

          
        llss = os.listdir(self.mainRoot)
        # Make project folders if they don't already exist
        if self.blocksRoot.split('/')[-2] not in llss:
            os.mkdir(self.blocksRoot)
        if self.resultsRoot.split('/')[-2] not in llss:
            os.mkdir(self.resultsRoot)
        if self.mssRoot.split('/')[-2] not in llss:
            os.mkdir(self.mssRoot)
       
    
   
    #==============================================================================================================#
    
    
    def getFileNames(self,dataRoot):
        '''
        Walks the filestructur below dataRoot and returns names and paths
        to all .h5 files.
        '''
        fileStructure = os.walk(dataRoot)
    
        h5Files = []
        for entry in fileStructure:
            thisPath = entry[0]
            thisFileList = entry[2]
            #print thisPath, thisFileList
    
            for ff in thisFileList:
                if ff.endswith('.h5'):
                    h5Files.append(os.path.join(thisPath,ff))
                if self.verbose:
                    print os.path.join(thisPath,ff)
        return h5Files
                
        

    #==============================================================================================================#
 
    def parallelExtractHDF5(self, bucketName = 'w205-msd', testMode = False, refresh = False):
        '''
        Fetches all files in bucketName and extracts the data of interest
        from them using the nodeToDict function.  Returns results and
        also stores results in self.results
        
        '''
        import multiprocessing as mp

        numCPUs = mp.cpu_count()

        multipool = mp.Pool(numCPUs)
        self.results = []
        
        if self.verbose:    
            print 'Extracting data from MSD HDF5 files...'

        bucketKeys = listS3Files(bucketName)
        
        
        for thisKey in bucketKeys:
            thisKey.localStorePath = self.mssRoot

            


        if testMode:
            bucketKeys = bucketKeys[0:testMode]

        print bucketKeys
        self.results = multipool.map(nodeToDict, bucketKeys)


        if self.verbose:        
            print 'Completed processing all bucket contents.'
    
        return self.results
    
    #==============================================================================================================#
    def transformHDF5(self, outCSVFileName = 'MSD_Flat.csv', bucketName = 'w205-msd'):
        '''
        Takes results from self.results, flattens them, and ensures that
        all columns are extracted.
        
        Writes csv file to outCSVFile name in the S3 bucket bucketName and in the
        local resultsRoot. Also returns results to caller.

        '''        
        import csv
    
        allParameters = []

        # Add bucket name to outCSVFile name so as not to overwrite good ones
        #outCSVFileName = 

        # Flatten results (comes in as a list of lists)
        self.flatResults = [item for sublist in self.results for item in sublist]
    
        # This loop gets all the names of the measurements (key, tempo,etc) making this code 
        # not dependent on every song having exactly the same structure
        for song in self.flatResults:
            if len(song)>0:    
                [allParameters.append(measure) for measure in song.keys()]
                allParameters = list(set(allParameters))   # keep only unique measurement names 
        
        # Write dictionaries as .csv file
        with open(os.path.join(self.resultsRoot,outCSVFileName), 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, allParameters)
            dict_writer.writeheader()
            dict_writer.writerows(self.flatResults)
    

        if self.verbose:
            print 'Pushing results to S3 Bucket ', bucketName
            
        putS3File(os.path.join(self.resultsRoot,outCSVFileName), bucketName)    
    
        print '\n\n\tComplete.  CSV written to ', os.path.join(self.resultsRoot,outCSVFileName), '\n\n'
        
        return self.flatResults
        
    #==============================================================================================================#
    
    def loadHDF5ToMySQL(self):
        # Import the flat csv file into pandas
        # This will facilitate any hands-on analyses we might want to do
        # And makes setting up a MySQL table REALLY easy
    
        import MySQLdb
        import pandas as pd
    
        # Connect to a local MySQL server using the username "root" (no password) 
        # and ensure the existance of the database mss.
        if self.verbose:
            print 'Ensuring database exists.'

        dbConnection=MySQLdb.connect(host="127.0.0.1",user="root")
        curse = dbConnection.cursor()
        dbsql = "CREATE DATABASE IF NOT EXISTS MSS"
        curse.execute(dbsql)
        curse.close()
        dbConnection.close()

        #Add user and create table mss
        #ausql = "CREATE USER metamusic" 
        #grantsql = "GRANT ALL PRIVILEGES ON *.* TO 'metamusic'@'127.0.0.1'"
        if self.verbose:
            print "Ensuring the MSS table exists in the MSS database"
        dbConnection=MySQLdb.connect(host="127.0.0.1",user="root",db="MSS")
        curse = dbConnection.cursor()
        tablesql = "CREATE TABLE IF NOT EXISTS MSS (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id))"
        curse.execute(tablesql)
        curse.close()

        # Turn our csv file into a Pandas data frame.  
        if self.verbose:
            print 'Loading ', os.path.join(self.resultsRoot,'MSD_Flat.csv'), ' into pandas data frame.'
        MSSdf = pd.read_csv(os.path.join(self.resultsRoot,'MSD_Flat.csv'))
    
        # Tell pandas to load this dataframe as a MySQL table
        if self.verbose:
            print 'Pushing data frame to MySQL database'

        typ = {'title':'VARCHAR(128)','release':'VARCHAR(128)','artist_name':'VARCHAR(128)'}  # Song titles often exceed the default length allocated by pandas

        # Clean up data to make MySQL happy
        MSSdf = MSSdf.astype(object).where(pd.notnull(MSSdf), None)
    
        # Send data to database--replace data if it already exists
        MSSdf.to_sql("MSS", con= dbConnection, flavor = 'mysql', if_exists = 'replace',dtype=typ)
        dbConnection.close()

    
         
#==============================================================================================================#

    def loadBillboardToMySQL(self,inputFile = 'billboard.csv'):
        import MySQLdb
        import pandas as pd

        dbConnection=MySQLdb.connect(host="127.0.0.1",user="root")
        curse = dbConnection.cursor()
        dbsql = "CREATE DATABASE IF NOT EXISTS MSS"
        curse.execute(dbsql)
        curse.close()
        dbConnection.close()

        #Add user and create table mss
        #ausql = "CREATE USER metamusic" 
        #grantsql = "GRANT ALL PRIVILEGES ON *.* TO 'metamusic'@'127.0.0.1'"
        dbConnection=MySQLdb.connect(host="127.0.0.1",user="root",db="MSS")
        curse = dbConnection.cursor()
        tablesql = "CREATE TABLE IF NOT EXISTS billboard (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id))"
        curse.execute(tablesql)
        curse.close()
        dbConnection.close()
        
        inputFile = os.path.join(self.resultsRoot,inputFile)
        typ = {'title':'VARCHAR(128)'}
        dfBillboard = pd.read_csv(inputFile)
        dfBillboard = dfBillboard.astype(object).where(pd.notnull(dfBillboard), None)
        dbConnection=MySQLdb.connect(host="localhost",user="james",db="mss")

        #Tell pandas to load this dataframe as a MySQL table
        dfBillboard.to_sql("billboard", con= dbConnection, flavor = 'mysql', if_exists = 'replace',dtype = typ)
    
        dbConnection.close()

#==============================================================================================================#
#==============================================================================================================#
    
def main():
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    parser.add_option("-t", "--test", action = "store", dest = "testMode", default=False)    
    
    (options, args) = parser.parse_args()
    
    if args:
        bucketName = args[0]
    else:
        bucketName = 'w205-msd'
    
    m = metaMusic()
    
    m.parallelExtractHDF5(bucketName=bucketName,verbose = options.verbose, testMode =options.testMode)
    m.transformHDF5(verbose = options.verbose)
    
    # 

        

#==============================================================================================================#
#==============================================================================================================#

if __name__ == "__main__":
    main()


