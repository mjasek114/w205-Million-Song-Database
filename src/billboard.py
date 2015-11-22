"""
author: Megan Jasek

Takes the full Billboard data and creates a tab delimited file with just the attributes:
    artist, song name, peak position and year of peak position that the project needs.
    
"""

#Create the input and output filenames to be used
inputFileName = 'Billboard Pop ME (1890-2011) 20110806.txt'
outputFileName = 'billboard.txt'

with open(inputFileName, 'r') as inFile:
    with open(outputFileName, 'w') as outFile:
        #read the first line and ignore it as that is the header line
        inLine = inFile.readline()
        #read the next line from the file
        inLine = inFile.readline()
        #i is a counter that keeps track of the line # in the file
        i=0
        #j is a counter that counts the number of valid lines.
        j=0
        while inLine != '':
            #split the line by tabs
            attrs = inLine.split('\t')
            #set the attributes that we are interested in to the appropriate fields from the file
            artist = attrs[10]
            name = attrs[16]
            peakposition = attrs[8]
            year = attrs[0]
            # do some testing to see if any the interesting fields are blank
            if artist == '':
                print("artist is blank")
                print(i)
            if name == '':
                print("name is blank")
                print(i)
            if peakposition == '':
                print("peakposition is blank")
                print(i)
            if year == '':
                print("year is blank")
                print(i)
            #if a line is valid (it has no blank fields) then write it to the file
            if artist != '' and name != '' and peakposition != '' and year != '':
                outLine = artist + '\t' + name + '\t' + peakposition + '\t' + year + '\n'
                outFile.write(outLine)
                j+=1
            #read the next line and increase the line counter
            inLine = inFile.readline()
            i += 1
            
#print how many lines were in the input file
print(i)
#print how many valid lines were written to the output file
print(j)
