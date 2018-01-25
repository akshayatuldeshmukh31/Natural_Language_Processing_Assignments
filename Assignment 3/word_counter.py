from collections import defaultdict
from csv import DictReader, DictWriter

import nltk
import codecs
import sys
import math
import re
from nltk.corpus import wordnet as wn
from nltk.tokenize import TreebankWordTokenizer

kTOKENIZER = TreebankWordTokenizer()
reader = codecs.getreader('utf8')
pron_dict = nltk.corpus.cmudict.dict()
old_english_words = ["thy","thou","thee","thine","doth","art","hath","dost","hast","thyself"]
common_english_words = {"more","shall","yet","should","not","no","do","nor","the","of","to","and","a","in","is","it","you","that","he","was","for","on","are","with","as","i","I","his","they","be","at","one","have","this","from","or","had","by","some","but","what","there","we","can","out","other","were","all","your","when","up","how","an","each","she","which","their","if","will","about","then","them","would","so","these","her","him","has","could","did","my","who","than","may","been","now","any","where","after","make","made","back","little","only","man","came","every","me","our","under","very","through","before","same","too","also","here","such","why","off","us","again","near","still","let","might","often","always","those","both","until","above","though","am"}

s_dict = defaultdict(int)
b_dict = defaultdict(int)

def morphy_stem(word):
    """
    Simple stemmer
    """
    stem = wn.morphy(word)
    if stem:
        return stem.lower()
    else:
        return word.lower()

def clip_text(tokenized_text):
    index = 0
    tokenized_text_len = len(tokenized_text)

    while index < tokenized_text_len:
        if not tokenized_text[index][0].isalpha():
            del tokenized_text[index]
            tokenized_text_len -= 1
            continue
        index += 1

    return tokenized_text

def features(text, cat = None):
    tokenized_text = kTOKENIZER.tokenize(text)
    tokenized_text = clip_text(tokenized_text)

    for i in range(len(tokenized_text)):
        tokenized_text[i] = morphy_stem(tokenized_text[i])

        if tokenized_text[i] not in common_english_words:
	        if cat == 's':
	        	s_dict[tokenized_text[i]] += 1
	        elif cat == 'b':
	        	b_dict[tokenized_text[i]] += 1    

    # for i in range(len(tokenized_text) - 1):
    # 	if cat == 's':
    # 		s_dict[tokenized_text[i] + "," + tokenized_text[i+1]] += 1
    # 	elif cat == 'b':
    # 		b_dict[tokenized_text[i] + "," + tokenized_text[i+1]] += 1

    return len(tokenized_text)

def clean_tokenized_text(tokenized_text):
	index = 0
	length = len(tokenized_text)

	while index < length:
		if not tokenized_text[index][0].isalpha():
			del tokenized_text[index]
			length -= 1
		else:
			index += 1

	return tokenized_text

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

def num_syllables(text):

	tokenized_text = kTOKENIZER.tokenize(text)
	tokenized_text = clean_tokenized_text(tokenized_text)

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

def count_punc(text):
	tokenized_text = kTOKENIZER.tokenize(text)
	tokenized_text = clean_tokenized_text(tokenized_text)

	count = 0

	for token in tokenized_text:
		count += len(token)
	return count

def count_chars_per_word(text):
	tokenized_text = kTOKENIZER.tokenize(text)
	tokenized_text = clean_tokenized_text(tokenized_text)

	count = 0

	for token in tokenized_text:
		count += len(token)
	return float(count)/float(len(tokenized_text))

def count_old_english_words(text):
	tokenized_text = kTOKENIZER.tokenize(text)
	tokenized_text = clean_tokenized_text(tokenized_text)

	count = 0

	for token in tokenized_text:
		if token in old_english_words:
			count += 1

	return count

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

train = DictReader(prepfile("train.tsv", 'r'), delimiter='\t')

avg_words_s = 0
avg_syllables_s = 0
num_s = 0
avg_words_b = 0
avg_syllables_b = 0
num_b = 0

avg_punc_s = 0
avg_punc_b = 0

avg_char_per_word_s = 0
avg_char_per_word_b = 0

syllable_count_s = list()
syllable_count_b = list()

punc_count_s = list()
punc_count_b = list()

char_per_word_s = list()
char_per_word_b = list()

for ii in train:
	if ii['cat']=='s':
		num_s += 1
		avg_words_s += features(ii['text'], ii['cat'])
		syllable_count_s.append(num_syllables(ii['text']))
		avg_syllables_s += syllable_count_s[-1]
		punc_count_s.append(count_punc(ii['text']))
		avg_punc_s += punc_count_s[-1]
		char_per_word_s.append(count_chars_per_word(ii['text']))
		avg_char_per_word_s += char_per_word_s[-1]
	else:
		num_b += 1
		avg_words_b += features(ii['text'], ii['cat'])
		syllable_count_b.append(num_syllables(ii['text']))
		avg_syllables_b += syllable_count_b[-1]
		punc_count_b.append(count_punc(ii['text']))
		avg_punc_b += punc_count_b[-1]
		char_per_word_b.append(count_chars_per_word(ii['text']))
		avg_char_per_word_b += char_per_word_b[-1]

avg_words_s = float(avg_words_s)/float(num_s)
avg_words_b = float(avg_words_b)/float(num_b)
avg_syllables_s = float(avg_syllables_s)/float(num_s)
avg_syllables_b = float(avg_syllables_b)/float(num_b)
avg_punc_s = float(avg_punc_s)/float(num_s)
avg_punc_b = float(avg_punc_b)/float(num_b)
avg_char_per_word_s = float(avg_char_per_word_s)/float(num_s)
avg_char_per_word_b = float(avg_char_per_word_b)/float(num_b)

std_s = 0
std_b = 0
std_syllable_s = 0
std_syllable_b = 0
std_punc_s = 0
std_punc_b = 0
std_char_per_word_s = 0
std_char_per_word_b = 0

std_old_english_words_s = 0
std_old_english_words_b = 0

old_english_words_s = 0
old_english_words_b = 0

for word in old_english_words:
	old_english_words_s += s_dict[word]
	old_english_words_b += b_dict[word]

old_english_words_s = float(old_english_words_s)/float(num_s)
old_english_words_b = float(old_english_words_b)/float(num_b)

train = DictReader(prepfile("train.tsv", 'r'), delimiter='\t')
# Calc variance
for ii in train:
	if ii['cat']=='s':
		std_s += math.pow(avg_words_s - features(ii['text']),2)
		std_old_english_words_s += math.pow(old_english_words_s - count_old_english_words(ii['text']),2)
	else:
		std_b += math.pow(avg_words_b - features(ii['text']),2)
		std_old_english_words_b += math.pow(old_english_words_b - count_old_english_words(ii['text']),2)

for i in range(len(syllable_count_s)):
	std_syllable_s += math.pow(avg_syllables_s - syllable_count_s[i], 2)

for i in range(len(syllable_count_b)):
	std_syllable_b += math.pow(avg_syllables_b - syllable_count_b[i], 2)

for i in range(len(punc_count_s)):
	std_punc_s += math.pow(avg_punc_s - punc_count_s[i], 2)

for i in range(len(punc_count_b)):
	std_punc_b += math.pow(avg_punc_b - punc_count_b[i], 2)

for i in range(len(char_per_word_s)):
	std_char_per_word_s += math.pow(avg_char_per_word_s - char_per_word_s[i], 2)

for i in range(len(char_per_word_b)):
	std_char_per_word_b += math.pow(avg_char_per_word_b - char_per_word_b[i], 2)

std_s = math.sqrt(float(std_s)/float(num_s))
std_b = math.sqrt(float(std_b)/float(num_b))
std_syllable_s = math.sqrt(float(std_syllable_s)/float(num_s))
std_syllable_b = math.sqrt(float(std_syllable_b)/float(num_b))
std_punc_s = math.sqrt(float(std_punc_s)/float(num_s))
std_punc_b = math.sqrt(float(std_punc_b)/float(num_b))
std_char_per_word_s = math.sqrt(float(std_char_per_word_s)/float(num_s))
std_char_per_word_b = math.sqrt(float(std_char_per_word_b)/float(num_b))
std_old_english_words_s = math.sqrt(float(std_old_english_words_s))/float(num_s)
std_old_english_words_b = math.sqrt(float(std_old_english_words_b))/float(num_b)

print "AVERAGE S: ", avg_words_s
print "AVERAGE B: ", avg_words_b
print "AVERAGE PHONETICS S: ", avg_syllables_s
print "AVERAGE PHONETICS B: ", avg_syllables_b
print "AVERAGE PUNCS S: ", avg_punc_s
print "AVERAGE PUNCS B: ", avg_punc_b
print "AVERAGE CHAR/WORD S: ", avg_char_per_word_s
print "AVERAGE CHAR/WORD B: ", avg_char_per_word_b
print "std_S: ", std_s
print "std_B: ", std_b 
print "std_S PHONETICS: ", std_syllable_s
print "std_B PHONETICS: ", std_syllable_b
print "std_S PUNCS: ", std_punc_s
print "std_B PUNCS: ", std_punc_b
print "std_S CHAR/WORD: ", std_char_per_word_s
print "std_B CHAR/WORD: ", std_char_per_word_b

print "\n\n"
print "OLD ENGLISH AVG S: ", old_english_words_s
print "OLD ENGLISH AVG B: ", old_english_words_b
print "OLD ENGLISH STD S: ", std_old_english_words_s
print "OLD ENGLISH STD B: ", std_old_english_words_b

s_dict = sorted(s_dict.iteritems(),key=lambda (k,v): v,reverse=True)
b_dict = sorted(b_dict.iteritems(),key=lambda (k,v): v,reverse=True)

b_words = list()

for tup in b_dict:
	flag = 0
	for tupj in s_dict:
		if tup[0]==tupj[0]:
			flag = 1
			break
	if flag==1:
		continue
	else:
		b_words.append(tup[0])

print "\n\n"
print b_words


print "\n\n"
print s_dict

print "\n\n"
print b_dict