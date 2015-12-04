# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:45:52 2015

@author: james
"""

import os
import os.path
import mm

def getFinishedFiles(localStoreRoot):
    
    allFiles = mm.listS3Files('w205-mmm')    
    
    
    
    for ff in allFiles:
        if 'merged' in ff.name and 'c652' in ff.name:
            mm.getS3File(ff,localStoreRoot)
#=============================================================================#    

def mergeFinishedFiles(localStoreRoot):
    # Assume all files in that directory are part of the final data set
    # Put shortest file first (this should contain the header rows--if not,
    # the data re-order wont' hurt anything)

    pathToFiles = os.path.join(localStoreRoot,'merged')
    dirFiles = os.listdir(pathToFiles)
    if 'allRecords.csv' in dirFiles:
        dirFiles.remove('allRecords.csv')
    
    filesInSizeOrder = []
    
    while len(dirFiles)>0:
        sizes = [os.path.getsize(os.path.join(pathToFiles,ff)) for ff in dirFiles]
        smallestIndex  = sizes.index(min(sizes))
        filesInSizeOrder.append(dirFiles[smallestIndex])
        dirFiles.pop(smallestIndex)

    outFileName = os.path.join(pathToFiles,'allRecords.csv')
    oFile = open(outFileName, 'w')
    
    for fn in filesInSizeOrder:
        thisFileName = os.path.join(pathToFiles,fn)
        thisReadFile = open(thisFileName, 'r')
        lines = thisReadFile.readlines()
        oFile.writelines(lines)
        thisReadFile.close()

    oFile.close()        
        
        
    
#=============================================================================#                

def loadDB(resultsRoot, verbose = True):

    # Import the flat csv files into pandas
    # This will facilitate any hands-on analyses we might want to do
    # And makes setting up a MySQL table REALLY easy
        
    import MySQLdb
    import pandas as pd
    
    # Connect to a local MySQL server using the username "root" (no password) 
    # and ensure the existance of the database mss.
    if verbose:
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
    if verbose:
        print "Ensuring the MSS table exists in the MSS database"
    dbConnection=MySQLdb.connect(host="127.0.0.1",user="root",db="MSS")
    curse = dbConnection.cursor()
    tablesql = "CREATE TABLE IF NOT EXISTS MSS (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id))"
    curse.execute(tablesql)
    curse.close()
    
    # Turn our csv file into a Pandas data frame.  
    if verbose:
        print 'Loading ', os.path.join(resultsRoot,'MSD_Flat.csv'), ' into pandas data frame.'
    MSSdf = pd.read_csv(os.path.join(resultsRoot,'MSD_Flat.csv'))
    
    # Tell pandas to load this dataframe as a MySQL table
    if verbose:
        print 'Pushing data frame to MySQL database'
    
    typ = {'title':'VARCHAR(128)','release':'VARCHAR(128)','artist_name':'VARCHAR(128)'}  # Song titles often exceed the default length allocated by pandas
    
    # Clean up data to make MySQL happy
    MSSdf = MSSdf.astype(object).where(pd.notnull(MSSdf), None)
    
    # Send data to database--replace data if it already exists
    MSSdf.to_sql("MSS", con= dbConnection, flavor = 'mysql', if_exists = 'replace',dtype=typ)
    dbConnection.close()

#=============================================================================#    

def writeHeaderFile(pathToFiles):
    
    fileName = 'headers.txt'

    oFile = open(os.path.join(pathToFiles,fileName),'w')
    headerContents = '"artist","title","writer","year","peakPosition ","billboardYear ","artistHotttness","songHotttness","danceability","key","tempo","duration","loudness","timeSignature"'
    headerContents += "\n"
    oFile.write(headerContents)
    oFile.close()
    
#=============================================================================#    
def schemaSQL():

    schemaString =  '''CREATE TABLE Song (
	artist VARCHAR(256),
	title VARCHAR(1024),
	writer VARCHAR(256),
	year INT,
	peakPosition INT,
	billboardYear INT,
	artistHotttness FLOAT,
	songHotttness FLOAT,
	danceability FLOAT,
	key VARCHAR(10),
	tempo FLOAT,
	duration FLOAT,
	loudness FLOAT,
	timeSignature INT
)'''
    return schemaString
#=============================================================================#    

def main():
    
    localStoreRoot = '/data/'
    
    print 'Ensuring appropriate local storage paths'

    try:    
        if not os.path.lexists(localStoreRoot):
            os.mkdir(localStoreRoot)
    
        if not os.path.lexists(os.join(localStoreRoot,'merged')):
            os.mkdir(os.join(localStoreRoot,'merged'))
        
        print 'Fetching finshed file(s) from bucket w205-mmm'

        getFinishedFile('/data/')

        return 1
        
    except:
        print 'Error fetching finshed file from bucket'
        return 0
        
        
    


#==============================================================================================================#
#==============================================================================================================#

if __name__ == "__main__":
    main()

