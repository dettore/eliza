
#	ELIZA/DOCTOR
#	CREATED BY JOSEPH WEIZENBAUM
#	THIS VERSION BY JEFF SHRAGER
#	EDITED AND MODIFIED FOR MITS 8K BASIC 4.0 BY STEVE NORTH
#	CREATIVE COMPUTING PO BOX 789-M MORRISTOWN NJ 07960

# Source: http://www.vintagecomputer.net/commodore/64/TOK64/ELIZA.txt
# Accessed: 20120310
# Author: STEVE NORTH
# Date written: ?1979?

# https://github.com/jeffshrager/elizagen.git
# eliza/versions/20120310ShragerNorthEliza.c64basic

# Recreation of the (C64?) BASIC version in Python

# Basic Outline and Flow of the BASIC Version
#
# 80 REM -----INITIALIZATION-----
#180 REM -----USER INPUT SECTION-----
#270 REM -----FIND KEYWORD IN I$-----
#1010 REM -----PROGRAM DATA FOLLOWS-----


import re


def regExMagic(pattern, string):
    objectMatch = re.search(pattern, string)
    return objectMatch


def readingLinesWithRegEx():
    try:
        dataStatementsCount = 0
        dataElementsCount = 0
        with open('20120310ShragerNorthEliza.c64basic') as file_object:
            contents = file_object.readlines()
            print('\n')
            for line in contents:

                #find if the pass line contains BASIC DATA statements
                #pattern is 4 digit line number followed by space then 'DATA'
                pattern = '(\d{4}) DATA'
                
                if str(regExMagic(pattern, line)) == "None":
                    # not a DATA statement
                    pass
                else:
                    # This is a DATA statement
                    # Strip off the '\n', and characters up to start of element 
                    line=line.strip()
                    dataStatementValue = line[10:len(line)]
                    dataStatements.append(dataStatementValue)
                    dataStatementsCount = dataStatementsCount + 1
                    
                    # Split out the elements from the DATA statement
                    # String elements may have ',' in value so split
                    # strings with '",'.
                    if dataStatementValue[0] == '"':
                        # Will remove split value from end of string
                        dataElementValue = dataStatementValue.split('",')
                    else:
                        dataElementValue = dataStatementValue.split(',')
                        
                    for element in range(0,len(dataElementValue)):
                        # Strip any remaining '"' from start of strings
                        dataElements.append(dataElementValue[element].strip('"'))
                        dataElementsCount = dataElementsCount + 1
                    
                    
    except OSError as booboo:
        print("We had a booboo!!")
        print(booboo)

    #print("\nFOUND " + str(dataStatementsCount) + " DATA STATEMENTS")
    #print("\nFOUND " + str(dataElementsCount) + " DATA ELEMENTS\n")

    
def getUserInput():
    # Have user tell Eliza their problem    
    patientInput = input("? ")

    # Keywords are all caps from BASIC so convert input, pad with spaces
    # and get rid of apostophes
    problem = " " + patientInput.upper() + "  "
    problem = problem.replace("'","")

    return problem


def findKeyword():

##    global dataPointer
##    global saveKeywordNumber
##    global textLocation
##    global foundKeyword

    # These variables are only available inside the function
    dataPointer=0  # Same as RESTORE
    saveKeywordNumber = -1  # Indicates NOKEYWORDFOUND
    textLocation = ''
    foundKeyword = ''
    
    for dataPointer in range(0,n1):
        if saveKeywordNumber > -1:
            pass
        elif dataElements[dataPointer] in problem:
            saveKeywordNumber = dataPointer
            textLocation = problem.find(dataElements[dataPointer])
            foundKeyword = dataElements[dataPointer]

    #return a tuple with the return values
    return saveKeywordNumber, textLocation, foundKeyword;


def conjugateString(text, keyword, location):

    dataPointer=36  # Start of Conjunctions

    # BASIC added +1 but not need in Python since we start at 0
    startInText = len(text)-len(keyword)-location
    conjugateText = " " + problem[-abs(startInText):len(text)]

    for dp in range(36,(36+n2),2):
            said=dataElements[dp]
            response=dataElements[dp+1]
            if said in conjugateText:
                conjugateText=conjugateText.replace(said, response)
            elif response in conjugateText:
                conjugateText=conjugateText.replace(response, said)
            
    # print(text)
    # print(conjugateText)
    
    if conjugateText.startswith(" ",1,2):        # 2 spaces at start
        conjugateText=" "+conjugateText.lstrip(" ")  # Only want one space
 
    return conjugateText;
    
    

# -----INITIALIZATION-----

dataStatements = []  # List with all of the DATA statememt lines
dataElements = []    # List with all of the individual data elements
dataPointer=0        # Same as RESTORE - Points to first data element

readingLinesWithRegEx()  # Load the DATA statements from the BASIC file

# Variables used to locate keyword and save location
saveKeywordNumber = -1
textLocation = ''
foundKeyword = ''

# define three lists to match BASIC arrays

s = []               # Appears to represent "said"       : DIM S(36)
rightReply = []      # Appears to represnet "reply"      : DIM R(36)
n = []               # Not sure what this represents yet : DIM N(36)

n1 = 36     # Count of total number of keywords / right reply pairs
n2 = 12     # Count of total number of conjugations
n3 = 112    # Count of total number of replies

# Same as RESTORE.  Skips to the start of the right replies data
for dataPointer in range(0,(n1+n2+n3)):
    z=str(dataElements[dataPointer])

dataPointer=dataPointer + 1

# Load the data for finding the right replies
for x in range(0,n1):
    s.append(int(dataElements[dataPointer])-1) # -1 adj for 0 start
    l = int(dataElements[dataPointer+1])
    rightReply.append(s[x])
    n.append(s[x] + l - 1)
    dataPointer=dataPointer+2


# -----USER INPUT SECTION-----

print("HI! I'M ELIZA. WHAT'S YOUR PROBLEM?")

previousProblem = ''  # Will hold what was previously said

while True:
    problem = getUserInput()
    
    # Check to see if the user said to shut up, which is to exit
    pattern = 'SHUT'

    if str(regExMagic(pattern, problem)) == "None":
        if problem == previousProblem:
            print("PLEASE DON'T REPEAT YOURSELF!")
        else:
            # Find Keyword
            saveKeywordNumber, textLocation, foundKeyword = findKeyword()
            # If found, conjugate the string
            if saveKeywordNumber > -1:
                keywordNumber = saveKeywordNumber
                locationInText = textLocation
                conjugatedString=conjugateString(problem, foundKeyword, locationInText)
                # print(conjugatedString)
            else:
                keywordNumber = 35  # Indicate NOKEYFOUND
            # Then build and print response
            dataPointer=n1+n2  # Start of resoponses
            #k=keywordNumber
            foundResponse=dataElements[dataPointer+rightReply[keywordNumber]]
            rightReply[keywordNumber]=rightReply[keywordNumber]+1
            if rightReply[keywordNumber]>n[keywordNumber]:
                rightReply[keywordNumber]=s[keywordNumber]

            if foundResponse[len(foundResponse)-1] != "*":
                print(foundResponse)
                previousProblem=problem
            else:
                print(foundResponse.replace("*",conjugatedString))
                previousProblem=problem
            
    else:
        print("OK, I'll SHUT UP...")
        break



