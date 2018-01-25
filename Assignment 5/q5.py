#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples
print "WORD - JACK"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['jack'],set(['jack']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - KITCHEN"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['kitchen'],set(['kitchen']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - LARGE"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['large'],set(['large']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - WALKED"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['walked'],set(['walked']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - HOSPITALS"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['hospitals'],set(['hospitals']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - AMOUNT"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['amount'],set(['amount']),distsim.cossim_dense), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""
