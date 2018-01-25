#!/usr/bin/env python
from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
import re
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

kTOKENIZER = TreebankWordTokenizer()
pron_dict = nltk.corpus.cmudict.dict()
old_english_words = {"thy","thou","thee","thine","doth","art","hath","dost","hast","thyself"}
common_english_words = {"not","no","do","nor","the","of","to","and","a","in","is","it","you","that","he","was","for","on","are","with","as","i","I","his","they","be","at","one","have","this","from","or","had","by","some","but","what","there","we","can","out","other","were","all","your","when","up","how","an","each","she","which","their","if","will","about","then","them","would","so","these","her","him","has","could","did","my","who","than","may","been","now","any","where","after","make","made","back","little","only","man","came","every","me","our","under","very","through","before","same","too","also","here","such","why","off","us","again","near","still","let","might","often","always","those","both","until","above","though","am"}

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

def guess_syllables(word):
    syllable_count = 0
    letter_position = list()
    word = word.strip().lower()

    for char in word:
        if char in ['a', 'e', 'i', 'o', 'u']:
            syllable_count += 1

    # Remove silent vowel - A
    temp_list = [m.start() for m in re.finditer("ally|ea|ae", word)]

    if len(temp_list)!=0:
        if (temp_list[0] == 0 and word=="ally") or (temp_list[0]==1 and word[1:5]=="ally"):
            syllable_count -= len(temp_list) + 1
            letter_position += temp_list[1:]
        else:
            syllable_count -= len(temp_list)
            letter_position += temp_list

    # Remove silent vowel - E
    temp_list = [m.start() for m in re.finditer("es$|e$", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                letter_position.append(pos)
                syllable_count -= 1

    # Remove silent vowel - I
    temp_list = [m.start() for m in re.finditer("ie|ai|ia|oi|ui|iu", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                letter_position.append(pos)
                syllable_count -= 1

    # Remove silent vowel - O
    temp_list = [m.start() for m in re.finditer("eo|oe|oo|ou", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                letter_position.append(pos)
                syllable_count -= 1

    # Remove silent vowel - U
    temp_list = [m.start() for m in re.finditer("ua|au|ue", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                letter_position.append(pos)
                syllable_count -= 1

    # Account for 'y' in the end
    temp_list = [m.start() for m in re.finditer("[^aeiou]y$", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                syllable_count += 1

    # Account for special case of silent 'e' in the end
    temp_list = [m.start() for m in re.finditer("[^aeiou][^aeiou]e$", word)]

    if len(temp_list)!=0:
        for pos in temp_list:
            if pos not in letter_position:
                syllable_count += 1

    return syllable_count

def num_syllables(tokenized_text):

    total_syllables = 0

    for word in tokenized_text:

        shortest_syllables = -1

        if(pron_dict.get(word, -1)!=-1):
            
            pronunciations_of_word = pron_dict[word]

            for pronunciation in pronunciations_of_word:
                count = 0
                for phone in pronunciation:
                    if phone[-1].isdigit():
                        count += 1
                if shortest_syllables==-1 or count < shortest_syllables:
                    shortest_syllables = count
        else:
            shortest_syllables = guess_syllables(word)

        total_syllables += shortest_syllables
    return total_syllables

def count_chars(tokenized_text):
    count = 0

    for token in tokenized_text:
        count += len(token)

    return count

def count_old_english_words(tokenized_text):
    count = 0

    for token in tokenized_text:
        if token in old_english_words:
            count += 1

    return count

class FeatureExtractor:

    def __init__(self):
        """
        You may want to add code here
        """

        None

    def clean_text(self, tokenized_text):
        index = 0
        tokenized_text_len = len(tokenized_text)

        while index < tokenized_text_len:
            if not tokenized_text[index][0].isalpha():
                del tokenized_text[index]
                tokenized_text_len -= 1
                continue
            index += 1

        return tokenized_text

    def features(self, text, train_mode = 0, train_cat = None):
        d = defaultdict(int)

        tokenized_text = kTOKENIZER.tokenize(text)
        tokenized_text = self.clean_text(tokenized_text)

        syllable_count = num_syllables(tokenized_text)
        character_count = count_chars(tokenized_text)
        old_english_word_count = count_old_english_words(tokenized_text)

        for i in range(len(tokenized_text)):
            tokenized_text[i] = morphy_stem(tokenized_text[i])

        for ii in tokenized_text:
            if ii not in common_english_words:
                d[ii] += 1

        d["WORD_COUNT"] += len(tokenized_text)
        d["SYLLABLE_COUNT"] += syllable_count
        d["CHAR_COUNT"] += character_count
        d["OLD_ENGLISH_COUNT"] += old_english_word_count

        return d
reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--trainfile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input train file")
    parser.add_argument("--testfile", "-t", nargs='?', type=argparse.FileType('r'), default=None, help="input test file")
    parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")
    parser.add_argument('--subsample', type=float, default=1.0,
                        help='subsample this fraction of total')
    args = parser.parse_args()
    trainfile = prepfile(args.trainfile, 'r')
    if args.testfile is not None:
        testfile = prepfile(args.testfile, 'r')
    else:
        testfile = None
    outfile = prepfile(args.outfile, 'w')

    # Create feature extractor (you may want to modify this)
    fe = FeatureExtractor()
    
    # Read in training data
    train = DictReader(trainfile, delimiter='\t')
    
    # Split off dev section
    dev_train = []
    dev_test = []
    full_train = []

    for ii in train:
        if args.subsample < 1.0 and int(ii['id']) % 100 > 100 * args.subsample:
            continue
        feat = fe.features(ii['text'], 1, ii['cat'])
        if int(ii['id']) % 5 == 0:
            dev_test.append((feat, ii['cat']))
        else:
            dev_train.append((feat, ii['cat']))
        full_train.append((feat, ii['cat']))

    # Train a classifier
    sys.stderr.write("Training classifier ...\n")
    classifier = nltk.classify.NaiveBayesClassifier.train(dev_train)

    right = 0
    total = len(dev_test)
    for ii in dev_test:
        prediction = classifier.classify(ii[0])
        if prediction == ii[1]:
            right += 1
        # else:
        #     print ii[0],ii[1]
        #     print "\n"

    sys.stderr.write("Accuracy on dev: %f\n" % (float(right) / float(total)))

    if testfile is None:
        sys.stderr.write("No test file passed; stopping.\n")
    else:
        # Retrain on all data
        classifier = nltk.classify.NaiveBayesClassifier.train(dev_train + dev_test)

        # Read in test section
        test = {}
        for ii in DictReader(testfile, delimiter='\t'):
            test[ii['id']] = classifier.classify(fe.features(ii['text']))

        print "\n\n"
        # Write predictions
        o = DictWriter(outfile, ['id', 'pred'])
        o.writeheader()
        for ii in sorted(test):
            o.writerow({'id': ii, 'pred': test[ii]})
