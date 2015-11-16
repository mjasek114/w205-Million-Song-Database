# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:22:50 2015

@author: james
"""

# From:
#   https://hdfgroup.org/wp/2015/03/from-hdf5-datasets-to-apache-spark-rdds/
# Specialized to MIDS W205-2 (Fall 2015)

# Modules needed below:
#   Pandas
#   h5py
#   psycopg2
#   MySQL-python
#   sqlalchemy

       
import os
import os.path
#import h5py
import sys
import sqlalchemy as sql

#==============================================================================================================#
#==============================================================================================================#

def nodeToDict(inputLine, verbose = True):
    '''
    This function is intended for use indirectly in Spark.
    Inputs a line (probably from the reference CSV)
    and extracts some important info 
    
    Returns a list of dictionaries, each dictionary has all "analysis" fields in the song.
    It's possible that all songs don't have exactly the same fields.
    '''
    import h5py

    parsedLine = inputLine.strip().split(',')
    songInfo = []
    try:

        if verbose:
            print 'Processing ', parsedLine[0]

        thisH5File = h5py.File(parsedLine[0])
        
        if parsedLine[0].split('/')[-1].startswith('Chunk'):
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
        print 'Error loading file ', parsedLine[0]
    
    return songInfo
    
#==============================================================================================================#
#==============================================================================================================#

class metaMusic:
    
    def __init__(self, minPartitions = 4, filesPerBlock = 100, verbose = True, autoRun = False):

        if verbose:
            print 'Setting up project folders.'
            
        self.verbose = verbose
        self.mainRoot = '/data/W205_Final/w205project/'
        self.mssRoot = '/data/W205_Final/w205project/data/'
        self.blocksRoot = '/data/W205_Final/w205project/blocks/'
        self.resultsRoot = '/data/W205_Final/w205project/resultsRoot/'
        self.results = None  # This is for holding the extraction results in memory
        self.filesPerBlock = filesPerBlock  # Gives about 30MB/file. Should use larger size in production.    
        self.minPartitions = minPartitions  #minimum number of partitions for use by Spark

          
        llss = os.listdir(self.mainRoot)
        # Make project folders if they don't already exist
        if self.blocksRoot.split('/')[-2] not in llss:
            os.mkdir(self.blocksRoot)
        if self.resultsRoot.split('/')[-2] not in llss:
            os.mkdir(self.resultsRoot)
        if self.mssRoot.split('/')[-2] not in llss:
            os.mkdir(self.mssRoot)
       
    
        # Configure spark to work
        if self.verbose:
            print 'Configuring Spark.'
    
        spark_home = os.environ.get('SPARK_HOME', None)
        if not spark_home:
            raise ValueError('SPARK_HOME environment variable is not set')
        sys.path.insert(0, os.path.join(spark_home, 'python'))
        sys.path.insert(0, os.path.join(spark_home, 'python/lib/py4j-0.8.2.1-src.zip'))
    
        if self.verbose:
            print 'Reading data'

        if autoRun:
            self.ETL_in_Spark()
            self.loadHDF5()
                
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

    def buildReferenceCSV(self, dataRoot = None, publish = True):
        '''
        Generates a text file containing file names and optionally
        writes them to file dataRoot/Hd5Files.csv
        '''
    
        if not dataRoot:
            dataRoot = self.blocksRoot
    
        h5Files = self.getFileNames(dataRoot)
    
        if publish:
            csvFileName = os.path.join(dataRoot,'Hd5Files.csv')
            oFile = open(csvFileName, 'w')
    
    
        for ff in h5Files:
        
            pubString = ff
    
            if publish:
                oFile.write(pubString + '\n')
    
            if self.verbose:
                print pubString
    
        return csvFileName
    
    #==============================================================================================================#

    #==============================================================================================================#
    def ETL_in_Spark(self):
        self.extractHDF5()
        self.transformHDF5()
        self.loadHDF5()

    def extractHDF5(self):        
        #  Processes in Spark
        #from pyspark import SparkContext
        import multiprocessing as mp

        numCPUs = mp.cpu_count()

        multipool = mp.Pool(numCPUs)
        self.results = []
        
        if self.verbose:    
            print 'Extracting data from MSS...'
            print '\tFetching all file names'

        self.buildReferenceCSV(publish=True)
    
        if self.verbose:
            print 'Extracting from HDF5 file.'

        extractFiles = open(os.path.join(self.blocksRoot,'Hd5Files.csv'))
        self.results = multipool.map(nodeToDict,extractFiles.readlines())

        if self.verbose:        
            print 'Results Generated.'
    
        #sc.stop
    
    #==============================================================================================================#
    def transformHDF5(self):
        # Get unique column names
        # and write results out as a csv
        import csv
    
        allParameters = []

        # Flatten results (comes in as a list of lists)
        self.results = [item for sublist in self.results for item in sublist]
    
        # This loop gets all the names of the measurements (key, tempo,etc) making this code 
        # not dependent on every song having exactly the same structure
        for song in self.results:
            if len(song)>0:    
                [allParameters.append(measure) for measure in song.keys()]
                allParameters = list(set(allParameters))   # keep only unique measurement names 
        
        # Write dictionaries as .csv file
        with open(os.path.join(self.resultsRoot,'MSD_Flat.csv'), 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, allParameters)
            dict_writer.writeheader()
            dict_writer.writerows(self.results)
    
        print '\n\n\tComplete.  CSV written to ', os.path.join(self.resultsRoot,'MSD_Flat.csv'), '\n\n'
    #==============================================================================================================#
    
    def loadHDF5(self):
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
        MSSdf = MSSdf.astype(object).where(pd.notnull(MSSdf), None)
        MSSdf.to_sql("MSS", con= dbConnection, flavor = 'mysql', if_exists = 'replace',dtype=typ)
        dbConnection.close()

    
         
#==============================================================================================================#

    def loadBillboard(self,inputFile = 'billboard.csv'):
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
    #from optparse import OptionParser
    #options,arguments = OptionParser.parse()    
    
    mm = metaMusic(autoRun=True)

        

#==============================================================================================================#
#==============================================================================================================#

if __name__ == "__main__":
    main()


