# -*- coding: utf-8 -*-
"""
@author: Peter
@class : CMSC416 Natural Language Processing
@assignment : 4
@due date : 03/26/2020

    Example run : 
            -> python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

Per grading rubric: 
    The Problem: 
    Actual Examples: 
        For general example, 
"""
from sys import argv
import re
import numpy as np
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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
    this = re.split(r'\s+', phrase)
    this = [word for word in this if not word in stopwords.words()]
    return this

def cleanIt(phrase):
    ''' Fix this to some method or something.'''
    phrase = re.sub('\$', '$ ', phrase) # Handle Dollar case
    phrase = re.sub("%", " % ", phrase) # Handle Percent Case
    phrase = re.sub('\-', " ", phrase) # Handle Hyphen Case
    phrase = re.sub('[\”|\“|\(|/)|\:|\;|\"|\’|!|,|\?|\'|‘]', '', phrase) # Destroy all quotes and some punctiation
    phrase = re.sub('</s>|</p>|<p>|<s>|<@>', '', phrase) # Handle carroted things
    phrase = re.sub(r'\. ', " ", phrase) # Handle punctuation that is followed by a space (EOL)
    phrase = re.sub('\.s ', "s ", phrase) # Handle punctuation followed by an s (Special Case)
    phrase = re.sub('/','',phrase) # Handle this case separately, at end
    phrase = re.sub("\s+" , " ", phrase) # Turn awkward spaces into single spaces
    sentence = phrase.lower() # DO THIS?
    return(sentence)

''' Handle command line arguments'''
train = str(argv[1]) 
test = str(argv[2])
k = 5
''' Preprocessing done here'''
File = open(train, 'r') # Open file
toAdd = File.read() # Read file
toAdd = re.sub('<[/]?context>\s|</instance>\s','', toAdd) # Successfully deletes all context lines
toAdd = toAdd.splitlines() # Split up everything by line

# We can get rid of every first line, every last line (That is a space), and every last 2 lines (Total of 3 last lines)
toAdd = toAdd[2:len(toAdd)-2] # This assumes last line as blank is required.
#print(toAdd[len(toAdd)-1]) # TEST for last line

# Handle the first line as target word? Will need to modify toAdd = toAdd[2:len(toAdd)-3] # This assumes last line as blank is required.

''' Ready to parse. Sets of 3 lines. First line, get instance ID. Second line, get senseID. Third line, get context.'''

numOfSets = len(toAdd)

phoneDict = {}
productDict = {}
features = {}
features = addFeatTypeKeys(features)

x = 0
while (x < numOfSets):
    # Should I remove the quotes for now?
    temp = re.search(r'".*"', toAdd[x]) # Successfully isolates key   INCLUDES QUOTES
    key = temp.group(0)
    temp2 = re.search(r'phone|product',toAdd[x+1]) # Successfully isolates sense    NO QUOTES
    sense = temp2.group(0)
    temp3 = toAdd[x+2]
    sentence = cleanIt(temp3)
    #print(sentence)
    # Pretty sure I don't need the below lines or those dictionaries anymore.
    if sense == "phone":
        phoneDict[key] = [sentence]
    elif sense == "product":
        productDict[key] = [sentence]
    else:
        print("Error!")
    x+=3

    tokens = tokenize(sentence)
    tokens = tokens[1:-1] # Adding a space at start and end of every one. Not sure why but easy fix with this!
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
        # print("Element " + str(y) + " of " + str(len(tokens)-1))
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
        # print("Element " + str(y) + " of " + str(len(tokens)-1))
        pass

    ''' +-k W Feature Type'''
    k0 = y-k
    kn = y+k
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
        # print(kTokens)
        pass

# for x1 in features:
#     print(str(x1))
#     print(features[x1])
rankings = {}
rankings["+1 W"] = {}
rankings["-1 W"] = {}
rankings["+-k W"] = {}
rankings["-2 -1"] = {}
rankings["-1 +1"] = {}
rankings["+1 +2"] = {}
sense1 = 'phone'
sense2 = 'product'

''' Solve and print Rankings '''
''' I am not confident the log math is correct considering I'm getting values over 1'''
for aFeatureType in features:
    for thisFeature in features[aFeatureType]:
        if(sense1 not in features[aFeatureType][thisFeature].keys()):
            features[aFeatureType][thisFeature][sense1] = 0
        if(sense2 not in features[aFeatureType][thisFeature].keys()):
            features[aFeatureType][thisFeature][sense2] = 0
        # The count of sense 1 given f_i
        A = features[aFeatureType][thisFeature][sense1]
        # The count of sense 2 given f_i
        B = features[aFeatureType][thisFeature][sense2]
        # f_i
        C = A+B
        if thisFeature not in rankings[aFeatureType]:
            rankings[aFeatureType][thisFeature] = {}
        # logA = 0.0002
        # logB = 0.0002
        # logC = 0.0002
        # if(A != 0):
        #     logA = math.log(A/C)
        # if(B != 0):
        #     logB = math.log(B/C)
        # if(C != 0):
        #     locC = math.log(C)
        alpha = 0.2
        A = A + alpha
        B = B + alpha
        C = C + alpha
        rankings[aFeatureType][thisFeature] = abs(math.log((A/C)/(B/C)))
        
        # rankings[aFeatureType][thisFeature] = abs(logA / logB)


rankedOutput = {}
for x1 in rankings:
    for x2 in rankings[x1]:
        rankedOutput[(x1,x2)] = rankings[x1][x2]

# Sorted rules that WORK
testRSorted = sorted(rankedOutput.items(), key=lambda x: (x[1],x[0]), reverse=True)

File2 = open("my-model.txt", "w+")
File2.write(" Log Probabilities. In the form (('Feature Type', 'Feature'), log probability)\n")
for x in testRSorted:
    File2.write(str(x) + "\n")

# for line in toAdd:
#     print(line)

''' So parse a sentence, get it's context. Now check each context. Sum the values, and the highest value is the answer '''
''' Preprocessing done here FOR TEST'''
File = open(test, 'r') # Open file
toAdd2 = File.read() # Read file
toAdd2 = re.sub('<[/]?context>\s|</instance>\s','', toAdd2) # Successfully deletes all context lines
toAdd2 = toAdd2.splitlines() # Split up everything by line

toAdd2 = toAdd2[2:len(toAdd2)-2] # This assumes last line as blank is required.

numOfSets = len(toAdd2)

features2 = {}
# testdict[instance][sense]
# testcontext[instance][featuretype][feature]
testdict = {}
testcontext = {}

x = 0
while (x < numOfSets):
    temp = re.search(r'".*"', toAdd2[x]) # Successfully isolates key   INCLUDES QUOTES
    key = temp.group(0)
    testdict[key] = {}
    testcontext[key] = {}
    testcontext[key] = addFeatTypeKeys(testcontext[key])
    temp2 = toAdd2[x+1]
    sentence2 = cleanIt(temp2)

    # print(sentence2)

    tokens = tokenize(sentence2)
    tokens = tokens[1:-1] # Adding a space at start and end of every one. Not sure why but easy fix with this!
    location = 1000
    # print(tokens)
    for y in range (0,len(tokens)):
        if tokens[y] == "<head>line<head>" or tokens[y] == "<head>lines<head>":
            location = y
    y = location
    #['+1 W' , '-1 W' , '+-k W' , '-2 -1' , '-1 +1' , '+1 +2']
    # Not get all the features and feature types
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
        kn = len(tokens)-1 # CHECK THIS -1
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
    x+=2

# for _ in testcontext:
#     print(testcontext[_])

threshold = 0
''' Math it '''
# for _ in testcontext:
#     print(testcontext[_])


''' what i need is a method that is going to get the tuple key like +1 W and WORD
    take those, and test if THIS context has WORD at +1W'''
Collection = {}

# solved = False
# while(not solved):
#     # iterate through my ranked list!
#     # testRSorted
#     for x in range (0, len(testRSorted)): #fix this it ugly
#         FT = testRSorted[x][0][0]
#         F = testRSorted[x][0][1]
#         solved = True
# for _ in testcontext:
#     print(_)

#<answer instance="line-n.w8_059:8174:" senseid="phone"/>

for _ in testcontext:
    toPrint = "<answer instance=" + str(_)+ " senseid=\""
    solved = False
    added = False
    thisSense = "phone" #baseline
    while (not solved):
        for x in testRSorted:
            FT = x[0][0]
            F = x[0][1]
            if F in testcontext[_][FT]: # This works for the array as well!
                # print("Found it with " + str(FT) + " and ( " + str(F) + " )" )
                if features[FT][F]["product"] > features[FT][F]["phone"]:
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
    print(toPrint)
        
''' OUTPUT!!! '''       






# for x in testcontext:
#     for x2 in testcontext[x]:
#         print(x2)
#         print(testcontext[x][x2])





# for x in toAdd2:
#     print(x)

    
'''-------------------------------------------------------------------------'''
'''---------------------------------MAIN------------------------------------'''
'''-------------------------------------------------------------------------'''