'''
Pseudocode for wsd.py 

Step 1 : Handle command line arguements. wsd.py as arg0, training file as arg1, test file as arg2

Step 2 : Focus on Training Data first.
         --> Clean and Preprocess

Step 3 : Create a multidimensional dictionary to hold all of the features, their sense, and the count.
         --> features[Feature Type][Feature Word(s)][Sense] : Count

Step 4 : For every line of training context, parse and fill (Step 3), removing and isolating needed things (Like the ID)

Step 5 : Rank the feature rules (AKA "tests")
         --> ABS ( LOG (    P(Sense 1 given Feature_i) / P(Sense 2 given Feature_i)                 ))
         --> Use alpha for smoothing (Add to Numerator/Denominator alpha between 0.1 and 0.25 per Yarowsky's paper.)

Step 6 : Preprocess and Clean Testing Data

Step 7 : Create new dictionary, storing the key ID, feature, and the word(s).
         --> new[Key ID][Feature Type] : Feature Word(s)

Step 8 : For every unique key in this dictionary, iterate through the ranked tests / rules. 
         Once a specific Feature Type , Feature Word(s) unique tuple is found in the rules (starting at the highest log value from (Step 5))
         use that rule to decide the sense, based on whichever sense has the higher count in the dictionary from (Step 3)
         --> Output this

Pseudocode for scorer.py

Step 1 : Intake files

Step 2 : Parse each file with regex to capture values

Step 3 : Iterate and calculate number of correct versus number total

Step 4 : Utilize Pandas/Numpy for Confusion Matrix output
'''