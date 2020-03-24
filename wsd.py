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

''' Turn any string into an array of tokens based on white space(+)
    Regex tools used : re.split on white space'''
def tokenize(phrase):
    return re.split('\s+', phrase)


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

# Key = instance id
# First value = type?
# Second Value = context string?

phoneDict = {}
productDict = {}
features = {}
features["+1 W"] = {}
features["-1 W"] = {}
features["+-k W"] = {}
features["-2 -1"] = {}
features["-1 +1"] = {}
features["+1 +2"] = {}


x = 0
while (x < numOfSets):
    # Should I remove the quotes for now?
    temp = re.search(r'".*"', toAdd[x]) # Successfully isolates key   INCLUDES QUOTES
    key = temp.group(0)
    temp2 = re.search(r'phone|product',toAdd[x+1]) # Successfully isolates sense    NO QUOTES
    sense = temp2.group(0)
    temp3 = toAdd[x+2]
    ''' Fix this to some method or something.'''
    temp3 = re.sub('\$', '$ ', temp3) # Handle Dollar case
    temp3 = re.sub("%", " % ", temp3) # Handle Percent Case
    temp3 = re.sub('\-', " ", temp3) # Handle Hyphen Case
    temp3 = re.sub('[\”|\“|\(|/)|\:|\;|\"|\’|!|,|\?|\'|‘]', '', temp3) # Destroy all quotes and some punctiation
    temp3 = re.sub('</s>|</p>|<p>|<s>|<@>', '', temp3) # Handle carroted things
    temp3 = re.sub(r'\. ', " ", temp3) # Handle punctuation that is followed by a space (EOL)
    temp3 = re.sub('\.s ', "s ", temp3) # Handle punctuation followed by an s (Special Case)
    temp3 = re.sub('/','',temp3) # Handle this case separately, at end
    temp3 = re.sub("\s+" , " ", temp3) # Turn awkward spaces into single spaces
    sentence = temp3.lower() # DO THIS?
    print(sentence)
    if sense == "phone":
        phoneDict[key] = [sentence]
    elif sense == "product":
        productDict[key] = [sentence]
    else:
        print("Error!")
    x+=3

    # Should I get my features now?
    tokens = tokenize(sentence)
    location = 1000
    for y in range (0,len(tokens)):
        if tokens[y] == "<head>line<head>" or tokens[y] == "<head>lines<head>":
            location = y
    y = location
    #['+1 W' , '-1 W' , '+-k W' , '-2 -1' , '-1 +1' , '+1 +2']
    ''' Dict[Feature Type][Feature][Sense] : Count '''
    
    ''' +1 W Feature Type'''
    # Feature never seen for this Feature Type
    if tokens[y+1] not in features['+1 W'].keys():
        features['+1 W'][tokens[y+1]] = {}
    # Feature seen, but not for this type
    if sense not in features['+1 W'][tokens[y+1]].keys():
        features['+1 W'][tokens[y+1]][sense] = 1
    # Feature seen, for this type. Just incrementing.
    else:
        features['+1 W'][tokens[y+1]] += 1
    
    ''' -1 W Feature Type'''
    # Feature never seen for this Feature Type
    if tokens[y-1] not in features['-1 W'].keys():
        features['-1 W'][tokens[y-1]] = {}
    # Feature seen, but not for this type
    if sense not in features['-1 W'][tokens[y-1]].keys():
        features['-1 W'][tokens[y-1]][sense] = 1
    # Feature seen, for this type. Just incrementing.
    else:
        features['-1 W'][tokens[y-1]] += 1
    
    ''' -2 -1 Feature Type'''
    temp21 = tokens[y-2] + " " + tokens[y-1]
    # Feature never seen for this Feature Type
    if temp21 not in features['-2 -1'].keys():
        features['-2 -1'][temp21] = {}
    # Feature seen, but not for this type
    if sense not in features['-2 -1'][temp21].keys():
        features['-2 -1'][temp21][sense] = 1
    # Feature seen, for this type. Just incrementing.
    else:
        features['-2 -1'][temp21] += 1

    ''' -1 +1 Feature Type'''
    temp11 = tokens[y-1] + " " + tokens[y+1]
    # Feature never seen for this Feature Type
    if temp11 not in features['-1 +1'].keys():
        features['-1 +1'][temp11] = {}
    # Feature seen, but not for this type
    if sense not in features['-1 +1'][temp11].keys():
        features['-1 +1'][temp11][sense] = 1
    # Feature seen, for this type. Just incrementing.
    else:
        features['-1 +1'][temp11] += 1

    ''' +1 +2 Feature Type'''
    temp12 = tokens[y+1] + " " + tokens[y+2]
    # Feature never seen for this Feature Type
    if temp12 not in features['+1 +2'].keys():
        features['+1 +2'][temp12] = {}
    # Feature seen, but not for this type
    if sense not in features['+1 +2'][temp12].keys():
        features['+1 +2'][temp12][sense] = 1
    # Feature seen, for this type. Just incrementing.
    else:
        features['+1 +2'][temp12] += 1

   
    
    





for line in toAdd:
    print(line)
'''-------------------------------------------------------------------------'''
'''---------------------------------MAIN------------------------------------'''
'''-------------------------------------------------------------------------'''