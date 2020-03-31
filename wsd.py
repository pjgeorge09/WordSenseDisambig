# -*- coding: utf-8 -*-
'''
@author: Peter
@class : CMSC416 Natural Language Processing
@assignment : 4
@due date : 03/26/2020

    Example run : 
            -> python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

Per grading rubric: 
    The Problem : 
            -> Intake data from a txt (formatted from .xml) , and utilizing either Naive Bayes or Decision List classifiers, perform
               Word Sense Disambiguation. Train on one file, test on a second, and compare it with a provided key to check accuracy later.
    Actual Examples: 
        For general example, 
            -> python3 wsd.py TrainingData.txt TestingData.txt WriteableFileForRules.txt > FormattedPredictions.txt
            Context of program example:
                -> "... cellular </>line</> for ..." --> learning based on the -1 W word "cellular" in training would imply the "sense" would be "phone"
                
'''
from sys import argv
import re
import numpy as np
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

''' A method to quickly add keys of each feature type.'''
def addFeatTypeKeys(aDict):
    aDict["+1 W"] = {}
    aDict["-1 W"] = {}
    aDict["+-k W"] = {}
    aDict["-2 -1"] = {}
    aDict["-1 +1"] = {}
    aDict["+1 +2"] = {}
    return aDict

''' Turn any string into an array of tokens based on white space(+)
    Regex tools used : re.split on white space'''
def tokenize(phrase):
    toReturn = re.split(r'\s+', phrase)
    toReturn = [word for word in toReturn if not word in stopwords.words()] # Also removes stop words!
    return toReturn[1:-1] # Adding a space at start and end of every one. Not sure why but easy fix with this!

''' General phrase-cleaning tailored to this assignment. Regex based.'''
def cleanIt(phrase):
    #TODO consolodate
    phrase = re.sub('\$', '$ ', phrase) # Handle Dollar case
    phrase = re.sub("%", " % ", phrase) # Handle Percent Case
    phrase = re.sub('\-', " ", phrase) # Handle Hyphen Case
    phrase = re.sub('[\”|\“|\(|/)|\:|\;|\"|\’|!|,|\?|\'|‘]', '', phrase) # Destroy all quotes and some punctiation
    phrase = re.sub('</s>|</p>|<p>|<s>|<@>', '', phrase) # Handle carroted things
    phrase = re.sub(r'\. ', " ", phrase) # Handle punctuation that is followed by a space (EOL)
    phrase = re.sub('\.s ', "s ", phrase) # Handle punctuation followed by an s (Special Case)
    phrase = re.sub('/','',phrase) # Handle this case separately, at end
    phrase = re.sub("\s+" , " ", phrase) # Turn awkward spaces into single spaces
    sentence = phrase.lower() 
    return(sentence)

def readAndSplit(aFileName):
    File = open(aFileName, 'r') # Open file
    toReturn = File.read() # Read file
    toReturn = re.sub('<[/]?context>\s|</instance>\s','', toReturn) # Successfully deletes all context lines
    toReturn = toReturn.splitlines() # Split up everything by line
    # We can get rid of every first line, every last line (That is a space), and every last 2 lines (Total of 3 last lines)
    toReturn = toReturn[2:len(toReturn)-2] 
    return toReturn

''' -------------------------------------------------------------------------------------------------------------------------------------------------------- '''
''' --------------------------------------------------------------------- MAIN ----------------------------------------------------------------------------- '''
'''--------------------------------------------------------------------------------------------------------------------------------------------------------- '''

''' Handle command line arguments'''
train = str(argv[1]) # Training Data
test = str(argv[2])  # Testing Data
''' Global Variables'''
k = 5 # Value of look-around 
sense1 = 'phone'
sense2 = 'product'
alpha = 0.2 # Adjustment factor

''' -------------------------------------------------------------------------------------------------------------------------------------------------------- '''
''' -------------------------------------------------------------------------------------------------------------------------------------------------------- '''
'''----------------------------------------------------------------- Training Data -------------------------------------------------------------------------- '''

toAdd = readAndSplit(train) # Preprocessing

''' Ready to parse. Sets of 3 lines. First line, get instance ID. Second line, get senseID. Third line, get context.'''
numOfSets = len(toAdd)
features = {}
features = addFeatTypeKeys(features)

x = 0
while (x < numOfSets):
    temp = re.search(r'".*"', toAdd[x]) # Successfully isolates key   INCLUDES QUOTES
    key = temp.group(0)
    temp2 = re.search(r'phone|product',toAdd[x+1]) # Successfully isolates sense    NO QUOTES
    sense = temp2.group(0)
    temp3 = toAdd[x+2]
    sentence = cleanIt(temp3)
    
    x+=3

    tokens = tokenize(sentence)
    location = 1000
    for y in range (0,len(tokens)):
        if tokens[y] == "<head>line<head>" or tokens[y] == "<head>lines<head>":
            location = y
    y = location
    #['+1 W' , '-1 W' , '+-k W' , '-2 -1' , '-1 +1' , '+1 +2']
    ''' Dict[Feature Type][Feature][Sense] : Count '''

    ''' +1 W Feature Type'''
    try:
        # Feature never seen for this Feature Type
        if tokens[y+1] not in features['+1 W'].keys():
            features['+1 W'][tokens[y+1]] = {}
        # Feature seen, but not for this type
        if sense not in features['+1 W'][tokens[y+1]].keys():
            features['+1 W'][tokens[y+1]][sense] = 1
        # Feature seen, for this type. Just incrementing.
        else:
            features['+1 W'][tokens[y+1]][sense] += 1
    except:
        # print("fail          +1 W")
        pass

    ''' -1 W Feature Type'''
    try:
        # Feature never seen for this Feature Type
        if tokens[y-1] not in features['-1 W'].keys():
            features['-1 W'][tokens[y-1]] = {}
        # Feature seen, but not for this type
        if sense not in features['-1 W'][tokens[y-1]].keys():
            features['-1 W'][tokens[y-1]][sense] = 1
        # Feature seen, for this type. Just incrementing.
        else:
            features['-1 W'][tokens[y-1]][sense] += 1
    except:
        # print("fail        -1 W")
        pass
    
    ''' -2 -1 Feature Type'''
    try:
        temp21 = tokens[y-2] + " " + tokens[y-1]
        # Feature never seen for this Feature Type
        if temp21 not in features['-2 -1'].keys():
            features['-2 -1'][temp21] = {}
        # Feature seen, but not for this type
        if sense not in features['-2 -1'][temp21].keys():
            features['-2 -1'][temp21][sense] = 1
        # Feature seen, for this type. Just incrementing.
        else:
            features['-2 -1'][temp21][sense] += 1
    except:
        # print("fail       -2 -1")
        pass

    ''' -1 +1 Feature Type'''
    try:
        temp11 = tokens[y-1] + " " + tokens[y+1]
        # Feature never seen for this Feature Type
        if temp11 not in features['-1 +1'].keys():
            features['-1 +1'][temp11] = {}
        # Feature seen, but not for this type
        if sense not in features['-1 +1'][temp11].keys():
            features['-1 +1'][temp11][sense] = 1
        # Feature seen, for this type. Just incrementing.
        else:
            features['-1 +1'][temp11][sense] += 1
    except:
        # print("fail        -1 +1")
        pass

    ''' +1 +2 Feature Type'''
    try:
        temp12 = tokens[y+1] + " " + tokens[y+2]
        # Feature never seen for this Feature Type
        if temp12 not in features['+1 +2'].keys():
            features['+1 +2'][temp12] = {}
        # Feature seen, but not for this type
        if sense not in features['+1 +2'][temp12].keys():
            features['+1 +2'][temp12][sense] = 1
        # Feature seen, for this type. Just incrementing.
        else:
            features['+1 +2'][temp12][sense] += 1
    except:
        # print("fail     +1 +2")
        pass

    ''' +-k W Feature Type'''
    k0 = y-k # Leftmost workable value
    kn = y+k # Rightmost workable value
    if k0 < 0:
        k0 = 0
    if kn > len(tokens):
        kn = len(tokens)-1 # CHECK THIS -1
    kTokens = tokens[k0:kn]
    if '<head>line<head>' in kTokens:
        kTokens.remove('<head>line<head>')
    if '<head>lines<head>' in kTokens:
        kTokens.remove('<head>lines<head>')
    try:
        # For every element in the list from k0 to kn, excluding y
        for z in kTokens:
            # If this word has never been seen for +-k W feature, init it
            if z not in features['+-k W'].keys():
                features['+-k W'][z] = {}
            # If this sense has never been seen with this feature, init it to 1
            if sense not in features['+-k W'][z].keys():
                features['+-k W'][z][sense] = 1
            # If this sense HAS been seen with this feature, increment it by one
            else:
                features['+-k W'][z][sense] += 1
    except:
        # print("fail    +-k W")
        pass
''' --------------------------------------------------------- End Training Data --------------------------------------------------------------------------- '''
''' ------------------------------------------------------------------------------------------------------------------------------------------------------- '''
''' ---------------------------------------------------------- Generate Rules ----------------------------------------------------------------------------- '''

rankings = {}
rankings = addFeatTypeKeys(rankings)
''' Rank the individual tests by taking the ratio of the log likelihood '''
for aFeatureType in features:
    for thisFeature in features[aFeatureType]:

        # Init values that are null to 0
        if(sense1 not in features[aFeatureType][thisFeature].keys()):
            features[aFeatureType][thisFeature][sense1] = 0
        if(sense2 not in features[aFeatureType][thisFeature].keys()):
            features[aFeatureType][thisFeature][sense2] = 0

        A = features[aFeatureType][thisFeature][sense1]        # The count of sense 1 given f_i
        B = features[aFeatureType][thisFeature][sense2]        # The count of sense 2 given f_i
        C = A+B                                                # f_i

        if thisFeature not in rankings[aFeatureType]:          # init features
            rankings[aFeatureType][thisFeature] = {}
        A = A + alpha
        B = B + alpha # Modify ABC by alpha to add small smoothing for 0 numerator/denominators
        C = C + alpha
        rankings[aFeatureType][thisFeature] = abs(math.log((A/C)/(B/C)))

# Reformat dictionary for easy sorting (Where 1 key is a tuple for lambda function)
rankedOutput = {}
for x1 in rankings:
    for x2 in rankings[x1]:
        rankedOutput[(x1,x2)] = rankings[x1][x2]

# Sorted rules
sortedRules = sorted(rankedOutput.items(), key=lambda x: (x[1],x[0]), reverse=True)
# Output rules to my-model.txt
File2 = open("my-model.txt", "w+")
File2.write(" Log Probabilities. In the form (('Feature Type', 'Feature'), log probability)\n")
for x in sortedRules:
    File2.write(str(x) + "\n")

''' -------------------------------------------------- Rules are complete --------------------------------------------------------------------------------- '''
''' ------------------------------------------------------------------------------------------------------------------------------------------------------- '''
'''----------------------------------------------------- Testing Data ------------------------------------------------------------------------------------- '''

toAdd2 = readAndSplit(test) # Preprocessing
numOfSets = len(toAdd2)
testcontext = {}

x = 0
while (x < numOfSets):
    temp = re.search(r'".*"', toAdd2[x]) # Successfully isolates key   INCLUDES QUOTES
    key = temp.group(0)

    testcontext[key] = {}
    testcontext[key] = addFeatTypeKeys(testcontext[key]) # Init all the dictionary keys

    context = toAdd2[x+1] # The sentence itself
    tokens = tokenize(cleanIt(context)) # Cleaned and tokenized
    
    location = 1000
    for y in range (0,len(tokens)):
        if tokens[y] == "<head>line<head>" or tokens[y] == "<head>lines<head>":
            location = y
    y = location
    #['+1 W' , '-1 W' , '+-k W' , '-2 -1' , '-1 +1' , '+1 +2']
    # Now get all the features and feature types
    ''' +1 W Feature Type'''
    try:
        testcontext[key]['+1 W'] = tokens[y+1]
    except:
        # print("+1 W failure")
        pass
    ''' -1 W Feature Type'''
    try:
        testcontext[key]['-1 W'] = tokens[y-1]
    except:
        # print("-1 W failure")
        pass
    ''' -2 -1 Feature Type'''
    try:
        temp21 = tokens[y-2] + " " + tokens[y-1]
        testcontext[key]['-2 -1'] = temp21
    except:
        # print("-2 -1 failure")
        pass
    ''' -1 +1 Feature Type'''
    try:
        temp11 = tokens[y-1] + " " + tokens[y+1]
        testcontext[key]['-1 +1'] = temp11
    except:
        # print("-1 +1 failure")
        pass
    ''' +1 +2 Feature Type'''
    try:
        temp12 = tokens[y+1] + " " + tokens[y+2]
        testcontext[key]['+1 +2'] = temp12
    except:
        # print("+1 +2 failure")
        pass
    ''' +-k W Feature Type'''
    k0 = y-k
    kn = y+k
    if k0 < 0:
        k0 = 0
    if kn > len(tokens):
        kn = len(tokens)-1 
    kTokens = tokens[k0:kn]
    if '<head>line<head>' in kTokens:
        kTokens.remove('<head>line<head>')
    if '<head>lines<head>' in kTokens:
        kTokens.remove('<head>lines<head>')
    try:
        # For every element in the list from k0 to kn, excluding y
        testcontext[key]['+-k W'] = kTokens
    except:
        # print("+-k W failure")
        pass
    x+=2 # Increment for this loop is by 2 because first line is the ID info, second line is the context.

'''---------------------------------------------------- Testing Data End ---------------------------------------------------------------------------------- '''
''' ------------------------------------------------------------------------------------------------------------------------------------------------------- '''
'''---------------------------------------------------------- Output -------------------------------------------------------------------------------------- '''

''' For every line of training, while not answered, parse the sorted rules.
    If a sorted rule is found in the test context, select the sense. '''
for _ in testcontext:
    toPrint = "<answer instance=" + str(_)+ " senseid=\"" # Formatting
    solved = False
    added = False
    thisSense = sense1 #baseline
    while (not solved):
        for x in sortedRules:
            FT = x[0][0] # Feature Type (Like "W +1")
            F = x[0][1]  # Feature (The word(s) found there)
            if F in testcontext[_][FT]: # This works for the array as well! Which is AWESOME btw.
                if features[FT][F][sense2] > features[FT][F][sense1]:
                    toPrint = toPrint + "product\"/>"
                    added = True
                else:
                    toPrint = toPrint + "phone\"/>"
                    added = True
                solved = True
                break
        solved = True
    if not added:
        toPrint = toPrint + "phone\"/>"
    print(toPrint) # Output to command line or file by > in Linux