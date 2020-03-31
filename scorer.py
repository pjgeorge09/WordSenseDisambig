# -*- coding: utf-8 -*-
'''
@author: Peter
@class : CMSC416 Natural Language Processing
@assignment : 4
@due date : 03/26/2020

    Example run : 
            -> python3 scorer.py my-line-answers.txt line-key.txt'''
from sys import argv
import re
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

''' Handle command line arguments'''
mine = str(argv[1]) 
key = str(argv[2])
''' Preprocessing done here'''
Mine = open(mine, 'r') # Open file
Key = open(key, 'r') 

Key = Key.read()
Key = Key.splitlines()

Mine = Mine.read()
Mine = Mine.splitlines()
MyList = []
KeyList = []

# for x in range(0, len(Key)):
#     if Mine[x] != Key[x]:
#         temp = re.search("senseid=\"((.*))\"", Mine[x]) # Successfully isolates key   INCLUDES QUOTES
#         temp2 = re.search("senseid=\"((.*))\"", Key[x]) # Successfully isolates key   INCLUDES QUOTES
#         print(str(temp.group(1)) + " " + str(temp2.group(1)) +" "+ str(x+1))

for x in range(0, len(Key)):
    temp = re.search("senseid=\"((.*))\"", Mine[x]) # Successfully isolates key   INCLUDES QUOTES
    temp2 = re.search("senseid=\"((.*))\"", Key[x]) # Successfully isolates key   INCLUDES QUOTES
    MyList.append(temp.group(1))
    KeyList.append(temp2.group(1))

# Calculate total correct
correct = 0
total = 0
for x in range(0 , len(KeyList)-1):
    if(MyList[x] == KeyList[x]):
        correct += 1
    total += 1

print("Number Correct : " + str(correct))
print("Number Total : " + str(total))
print("Percent : " + str(correct*100/total))

# Calculate the confusion matrix. Requires 1D list comp (which is used)
y_actu = pd.Series(KeyList, name='Actual')
y_pred = pd.Series(MyList, name='Predicted')
df_confusion = pd.crosstab(y_actu, y_pred)
pd.set_option('display.expand_frame_repr', False)
print("\nConfusion matrix:\n%s" % df_confusion)