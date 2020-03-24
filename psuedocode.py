'''
PSUEDOCODE FOR WSD.PY (And scorer.py?)

Step 1 : Handle command line arguements. wsd.py as arg0, training file as arg1, test file as arg2

Step 2 : Open file and read in lines

Step 3 : Start with Training. Clean file. Remove unwanted things. (First line and last 3 lines)
            IMPORTANT. Files all have a single blank line at the end. This is removed and required. Preprocessing required if format changes. May automate later.

Step 4 : 






FOR EVERY SET, WE NEED EVERYTHING TO THE RIGHT OF "INSTANCE ID =" TO BE SAVED
REMOVE <CONTEXT>
PARSE CONTEXT LINE
        REGEX REMOVE ' <s> ' AND '<head>' AND </head>
        CONSIDER REMOVING SENTENCE CHARATS 
            FEATURES
                GET WORD IMMEDIATELY TO RIGHT
                GET WORD IMMEDIATELY TO LEFT
                GET K WORD WINDOW, + / - 4 OR 5 WORDS FROM WORD 0 AKA TARGET WORD
                GET PAIR OF WORDS AT OFFSET -2 AND -1
                GET PAIR OF WORDS AT OFFSET -1 AND +1
                GET PAIR OF WORDS AT OFFSET +1 AND +2
                ***CRITICAL PROCESS STEPS***
                    Just record the word window first. Tokenize this.
                    Method or methods to put word into features.
                    ex)   dict[thisID] : { -1 , 1 , (1 or 0)...(1 or 0), -2+" "+-1 , -1+" "+1, 1+" "+2}
                    
REMOVE </CONTEXT>
REMOVE </INSTANCE>

NOW GENERATE RULE TABLE USING DECISION LIST LIKE LECTURE 9 SLIDE 81



























'''