#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys
import os
import re
import math

#value is the string value of the field
# +++your code here+++
# Define print_words(filename) and print_top(filename) functions.
# You could write a helper utility function that reads a file
# and builds and returns a word/count dict for it.
# Then print_words() and print_top() can just call the utility function.

def tf(foldername):
    #dlist: filepath, dictionary
    dlist = {}
    df = {}
    #dict: tf, idf, tfidf
    #loop in one file
    for filepath in foldername:
        dict = {}
        input_file = open(filepath, 'r')
        for line in input_file:
            line = re.sub('[^0-9a-zA-Z]+', ' ', line)
            words = line.split()
            for word in words:
                word = word.lower()
                if len(word) > 2:
                    if word in dict:
                        dict[word] =(dict[word][0] + 1, 0, 0)
                    else:
                        dict[word] = (1, 0, 0)
        for word in dict:
            if word in df:
                df[word] = df[word] + 1
            else:
                df[word] = 1
        dlist[filepath] = dict
        #print dict
    #end loop
    #print df


    #calculate log-weighted term frequency: 1+log(tf)
    #and the log-weighted inverse document frequency: log (N/df)
    #and TFIDF = tf*idf
    #and normalized
    for filepath in dlist:
        for word in dlist[filepath]:
            dlist[filepath][word] = (1 + math.log10(dlist[filepath][word][0]), math.log10(len(dlist)/(df[word]*1.0)), 0)
           # print len(dlist), df[word],math.log10(len(dlist)/(df[word]*1.0))
            dlist[filepath][word] = (dlist[filepath][word][0], dlist[filepath][word][1], dlist[filepath][word][0] * dlist[filepath][word][1])
        normalize(dlist[filepath])
        #print dlist[filepath]
    input_file.close()
    return dlist

def normalize(dict):
    sum = 0
    #get the square sum of the  tf-idf
    for term in dict:
        sum = sum + math.pow(dict[term][2], 2.0)
    sum = math.sqrt(sum)
    #normalize the tf-idf
    for term1 in dict:
        dict[term1]= (dict[term1][0], dict[term1][1], dict[term1][2]/(sum*1.0))
        #print dict[term1][2]/(sum*1.0)
def normalizequery(dict):
    sum = 0
    #get the square sum of the  tf-idf
    for term in dict:
        sum = sum + math.pow(dict[term], 2.0)
    sum = math.sqrt(sum)
    #normalize the tf-idf
    for term1 in dict:
        dict[term1]= dict[term1]/(sum*1.0)


def tfquery(filename):
    dict = {}
    input_file = open(filename, 'r')
    for line in input_file:
        line = re.sub('[^0-9a-zA-Z]+', ' ', line)
        words = line.split()
        for word in words:
            word = word.lower()
            if len(word) > 2:
                if word in dict:
                    dict[word] =dict[word] + 1
                else:
                    dict[word] = 1
    normalizequery(dict)
    #print dict
    input_file.close()
    return dict


def rank(foldername, filename):
    dlist = tf(foldername)
    dict = tfquery(filename)

    #calcuate cosine score for each doc
    #score: filepath, cosine score
    score = {}
    for filepath in dlist:
        sum = 0
        for word in dict:
            if word in dlist[filepath]:
                sum = sum + dlist[filepath][word][2] * dict[word]
        score[filepath] = sum

    #for file in score:
        #if file == "reviews/cv032_22550.txt": print score[file]
    #output top5 document
    items = sorted(score.items(), key = lambda score: score[1], reverse = True)
    n = 1
    for item in items[:5]:
        print "%(num)s. %(item0)s (score is %(item1)s)" % {"num": n, "item0": item[0], "item1": item[1]}
        n += 1

@app.route('/print_top/')
def print_top(foldername):
    dict = tf(foldername)
    items = sorted(dict.items(), key = lambda dict: dict[1], reverse = True)
    n = 1
    for item in items[:5]:
        print "%(num)s. %(item0)s (frequency is %(item1)s)" % {"num": n, "item0": item[0], "item1": item[1]}
        n += 1
    return 'print top'
    return render_template('searchbytags.html')

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 3:
        print 'python query.py foldername filename'
        sys.exit(1)

    folder = sys.argv[1]
    file = sys.argv[2]

    file_paths = []
    filelist = os.listdir(folder)
    for filename in filelist:
        dic_name = folder + '/'
        path_txt= dic_name+ filename
        file_paths.append(path_txt)
    #print file_paths
    rank(file_paths, file)






if __name__ == '__main__':
    app.run()
