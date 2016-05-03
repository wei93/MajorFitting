#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import numpy
import math
import string
import operator
from collections import defaultdict

# n-gram lengths to iterate through
min_N = 1       # inclusive
max_N = 5      # exclusive

####  HELPER FUNCTIONS

# returns a dict mapping each n-gram that appears in the corpus to its frequency in the corpus
def ngram_freqs(corpus, n):
    
    # generate a list of all n-grams in the corpus
    ngrams = []
    for i in range(n, len(corpus)):
        ngrams += [tuple(corpus[i-n:i])]

    # count the frequency of each n-gram
    freq_dict = defaultdict(int)
    for ngram in ngrams:
        freq_dict[ngram] += 1
    
    return freq_dict

# combines two dicts by performing the provided operation on their values
def combine_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() + [(k, op(a[k], b[k])) for k in set(b) & set(a)])

# checks whether two n-grams overlap too much to include both
def overlap(a, b):
    max_overlap = min(3, len(a), len(b))
    overlap = False

    if '-'.join(a[:max_overlap]) in '-'.join(b):
        overlap = True
    if '-'.join(a[-max_overlap:]) in '-'.join(b):
        overlap = True
    if '-'.join(b[:max_overlap]) in '-'.join(a):
        overlap = True
    if '-'.join(b[-max_overlap:]) in '-'.join(a):
        overlap = True
    
    return overlap

####  ANALYSIS FUNCTIONS

# returns a list of corpora, each a sequential list of all words in one department
def corpus_list_from_file(foldername):
    corpus_list = []
    index = 0
    for filename in foldername:
         corpus_list += [[]]

    for filename in foldername:
        # load all words from the file into memory
        words = open(filename).read().split()

        for word in words:
            # remove punctuation and convert to lowercase
            word = word.translate(string.maketrans("",""), string.punctuation).lower()

            if word is not "":
                corpus_list[index] += [word]
        index += 1
    return corpus_list

# returns a list of dicts, each mapping an n-gram to its frequency in the respective corpus
def freq_dicts_from_corpus_list(corpus_list, foldername):
    freq_dicts = []
    for filename in range(len(foldername)):
        freq_dicts += [defaultdict(int)]

    # iteratively add all n-grams
    for n in range(min_N, max_N):
        for filename in range(len(foldername)):
            corpus = corpus_list[filename]
            dict_to_add = ngram_freqs(corpus, n)
            freq_dicts[filename] = combine_dicts(freq_dicts[filename], dict_to_add)
    #print freq_dicts
    return freq_dicts


# returns a list of dicts, each mapping an n-gram to its tf-idf in the respective corpus
# see https://en.wikipedia.org/wiki/Tf-idf for further information
def tfidf_dicts_from_freq_dicts(freq_dicts, foldername):
    
    # initialize the list of dicts
    tfidf_dicts = []
    for filename in range(len(foldername)):
        tfidf_dicts += [defaultdict(int)]
    
    # create a dict that maps an n-gram to the number of corpora containing that n-gram
    num_containing = defaultdict(int)
    for filename in range(len(foldername)):
        for ngram in freq_dicts[filename]:
            num_containing[ngram] += 1
    
    # calculate tf-idf for each n-gram in each corpus
    for filename in range(len(foldername)):
        for ngram in freq_dicts[filename]:
            tf = freq_dicts[filename][ngram]
            idf = math.log(len(foldername) / num_containing[ngram])
            
            # normalize by length of n-gram
            tfidf_dicts[filename][ngram] = tf * idf * len(ngram)
            
            # kill anything ending in "and" "or" "of" "with"

            if ngram[-1] in ["and", "or", "of", "with"]:
                tfidf_dicts[filename][ngram] = 0

    #print tfidf_dicts
    return tfidf_dicts

# kills any phrase (tfidf=0) contained inside a larger phrase with a higher score
def prune_substrings(tfidf_dicts, foldername, prune_thru=1000):
    
    pruned = tfidf_dicts
    for filename in range(len(foldername)):
        so_far = []
        
        ngrams_sorted = sorted(tfidf_dicts[filename].items(), key=operator.itemgetter(1), reverse=True)[:prune_thru]
        for ngram in ngrams_sorted:
            # contained in a previous aka 'better' phrase
            for better_ngram in so_far:
                if overlap(list(better_ngram), list(ngram[0])):
                    
                    pruned[filename][ngram[0]] = 0
            else:
                so_far += [list(ngram[0])]
    return pruned 

# sorts the n-grams by tf-idf
def top_ngrams_for_candidate(tfidf_dicts, filename, count=20):
    return sorted(tfidf_dicts[filename].items(), key=operator.itemgetter(1), reverse=True)[:count]


def main():
    file_paths = []
    filelist = os.listdir("ratemyprofessorsdata")
    for filename in filelist:
        dic_name = "ratemyprofessorsdata" + '/'
        path_txt = dic_name+ filename
        file_paths.append(path_txt)

    corpus_list = corpus_list_from_file(file_paths)
    freq_dicts = freq_dicts_from_corpus_list(corpus_list, file_paths)
    tfidf_dicts = tfidf_dicts_from_freq_dicts(freq_dicts, file_paths)
    tfidf_dicts = prune_substrings(tfidf_dicts, file_paths)

    # print the top ngrams sorted by tfidf
    os.getcwd()
    os.mkdir("rankresult(5 words)")
    os.chdir("rankresult(5 words)")
    i = 0
    for filename in range(len(file_paths)):
        fo = open(file_paths[filename][17:], 'a')
        #fo = open('t' + str(i) + '.txt', 'a')
        print file_paths[filename]
        for ngram in top_ngrams_for_candidate(tfidf_dicts, filename, 50):
            n = str(ngram)
            fo.write(repr(n)+ '\n')
        i = i + 1
        fo.close

    
    
if __name__ == '__main__':
    
    main()
    