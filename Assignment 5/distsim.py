from __future__ import division
import sys,json,math
import os
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    # Take two context-count dictionaries as input
    # and return the cosine similarity between the two vectors.
    # Should return a number beween 0 and 1

    ## TODO: delete this line and implement me

    # print type(v1)
    norm_v1 = 0.0
    norm_v2 = 0.0
    correlation = 0.0

    for key,value in v1.items():
        if v2.get(key, -1)!=-1:
            correlation += (value * v2[key])
        norm_v1 += pow(value, 2)

    for key,value in v2.items():
        norm_v2 += pow(value, 2)

    return (correlation)/(pow(norm_v1, 0.5) * pow(norm_v2, 0.5))

def cossim_dense(v1,v2):
    # v1 and v2 are numpy arrays
    # Compute the cosine simlarity between them.
    # Should return a number between -1 and 1
    
    ## TODO: delete this line and implement me
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    correlation = np.multiply(v1,v2).sum()

    return (correlation)/(norm_v1 * norm_v2)

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
    #word_2_vec: a dictionary of word-context vectors. The vector could be a sparse (dictionary) or dense (numpy array).
    #w_vec: the context vector of a particular query word `w`. It could be a sparse vector (dictionary) or dense vector (numpy array).
    #exclude_w: the words you want to exclude in the responses. It is a set in python.
    #sim_metric: the similarity metric you want to use. It is a python function
    # which takes two word vectors as arguments.

    # return: an iterable (e.g. a list) of up to 10 tuples of the form (word, score) where the nth tuple indicates the nth most similar word to the input word and the similarity score of that word and the input word
    # if fewer than 10 words are available the function should return a shorter iterable
    #
    # example:
    #[(cat, 0.827517295965), (university, -0.190753135501)]
    
    ## TODO: delete this line and implement me

    most_similar_words = list()

    for key,value in word_2_vec.items():
        if key not in exclude_w:
            most_similar_words.append((key, sim_metric(w_vec, value)))

    most_similar_words.sort(key=lambda x: x[1], reverse=True)
    return most_similar_words[:10]
    