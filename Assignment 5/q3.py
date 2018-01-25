#!/usr/bin/env python
import distsim

# you may have to replace this line if it is too slow 
word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below

###Answer examples

print "WORD - JACK"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['jack'],set(['jack']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - KITCHEN"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['kitchen'],set(['kitchen']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - LARGE"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['large'],set(['large']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - WALKED"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['walked'],set(['walked']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - HOSPITALS"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['hospitals'],set(['hospitals']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""

print "WORD - AMOUNT"
for i, (word, score) in enumerate(distsim.show_nearest(word_to_ccdict, word_to_ccdict['amount'],set(['amount']),distsim.cossim_sparse), start=1):
    print("{}: {} ({})".format(i, word, score))
print ""