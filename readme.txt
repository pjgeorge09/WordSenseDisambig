Programming Assignment 4 (due Tuesday 24 March 2020) 

Write a python program called wsd.py that implements either a Naïve Bayes or Decision List classifier to perform word sense disambiguation.

Your program should use the features described in Yarowsky’s paper and as many additional features as you think will result in an accurate classifier. Please make sure you only identify features from the training data, and that you clearly explain what features you are using in your detailed comments.

Your classifier should run from the command line as follows:

python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

This command should learn a model from line-train.txt and apply that to each of the sentences found in line-test.txt in order to assign a sense to the word line. Do not use line-test.txt in any other way (and only identify features from line-train.txt). Your program should output the model it learns to my-model.txt. You may format your model as you wish, but please make sure to show each feature, the log-likelihood or Bayes score associated with it, and the sense it predicts. The file my-model.txt is intended to be used as a log file in debugging your program. Your program should output the answer tags it creates for each sentence to STDOUT. Your answer tags should be in the same format as found in line-key.txt.

line-train.txt contains examples of the word line used in the sense of a phone line and a product line where the correct sense is marked in the text (to serve as an example from which to learn). line-test.txt contains sentences that use the word line without any sense being indicated, where the correct answer is found in the file line-key.txt. You can find line-train.txt and line-test.txt in the files section of our site in a compressed directory called line-data.zip.

Your program wsd.py should learn its model from line-train.txt and then apply that to line-test.txt.

You should also write a utility program called scorer.pl which will take as input your sense tagged output and compare it with the gold standard "key" data which I have placed in the Files section of our group (line-key.txt). Your scorer program should report the overall accuracy of your tagging, and provide a confusion matrix similar.  This program should write output to STDOUT.

The scorer program should be run as follows:

python3 scorer.py my-line-answers.txt line-key.txt

You can certainly use your scorer.py program from the previous assignment as a foundation for this program.

Both wsd.py and scorer.py should be documented according to the standards of the programming assignment rubric.

In wsd.py: include what model you implemented, your accuracy and confusion matrix into the comments. And compare your results to that of the most frequeant sense baseline.

Please submit your program source code for both wsd.py and scorer.py to the Blackboard.
