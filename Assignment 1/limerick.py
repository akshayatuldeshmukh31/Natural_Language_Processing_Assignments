#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

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

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!

        if(self._pronunciations.get(word, -1)!=-1):

        	shortest_syllables = -1

        	pronunciations_of_word = self._pronunciations[word]

        	for pronunciation in pronunciations_of_word:
        		count = 0
        		for phone in pronunciation:
        			if phone[-1].isdigit():
        				count += 1
        		if shortest_syllables==-1 or count < shortest_syllables:
        			shortest_syllables = count

        	return shortest_syllables

        return 1

    def isolate_after_first_vowel(self, word_pronunciations):
    	# Remove first consonant and previous sounds
        for pronunciation in word_pronunciations:
        	
        	first_vowel = -1
        	for i in range(len(pronunciation)):
        		if pronunciation[i][0] not in ['A', 'E', 'I', 'O', 'U']:
        			first_vowel = i
        		else:
        			break

        	if first_vowel!=-1:
        		del pronunciation[:first_vowel + 1]

        return word_pronunciations

    def check_phonetics_for_rhymes(self, a_pronunciation, b_pronunciation):

    	a_ind = len(a_pronunciation) - 1
    	b_ind = len(b_pronunciation) - 1

    	while(a_ind!=-1 and b_ind!=-1):
    		if(a_pronunciation[a_ind]!=b_pronunciation[b_ind]):
    			return False
    		a_ind -= 1
    		b_ind -= 1

    	return True

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # TODO: provide an implementation!
        if self._pronunciations.get(a, -1)==-1 or self._pronunciations.get(b, -1)==-1:
        	return False

        a_pronunciations = self._pronunciations[a]
        b_pronunciations = self._pronunciations[b]

        a_pronunciations = self.isolate_after_first_vowel(a_pronunciations)
        b_pronunciations = self.isolate_after_first_vowel(b_pronunciations)

        for a_pronunciation in a_pronunciations:
        	for b_pronunciation in b_pronunciations:

        		if len(a_pronunciation) <= len(b_pronunciation):
        			if self.check_phonetics_for_rhymes(a_pronunciation, b_pronunciation):
        				return True
        		elif self.check_phonetics_for_rhymes(b_pronunciation, a_pronunciation):
        			return True

        return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
        processed_text = text.split("\n")
        processed_text = [word_tokenize(line.strip()) for line in processed_text if len(line.strip())!=0]

        if len(processed_text)!=5:
        	return False

        for line in processed_text:
        	word_ind = 0
        	while word_ind<len(line):
        		count = 0
        		for char in line[word_ind]:
        			if not char.isalpha():
        				count += 1

        		if count==len(line[word_ind]):
        			del line[word_ind]
        			word_ind = 0
        			continue
        		word_ind += 1

        total_syllables_first_line = 0
        total_syllables_second_line = 0
        total_syllables_third_line = 0
        total_syllables_fourth_line = 0
        total_syllables_fifth_line = 0
        min_syllables = 0
        min_a_line_syllables = 0
        max_b_line_syllables = 0

        for word in processed_text[0]:
        	total_syllables_first_line += self.num_syllables(word)
        min_syllables = total_syllables_first_line
        min_a_line_syllables = total_syllables_first_line

        for word in processed_text[1]:
        	total_syllables_second_line += self.num_syllables(word)
        min_syllables = min(min_syllables, total_syllables_second_line)
        min_a_line_syllables = min(min_a_line_syllables, total_syllables_second_line)

        for word in processed_text[2]:
        	total_syllables_third_line += self.num_syllables(word)
        min_syllables = min(min_syllables, total_syllables_third_line)
        max_b_line_syllables = total_syllables_third_line

        for word in processed_text[3]:
        	total_syllables_fourth_line += self.num_syllables(word)
        min_syllables = min(min_syllables, total_syllables_fourth_line)
        max_b_line_syllables = max(max_b_line_syllables, total_syllables_fourth_line)

        for word in processed_text[4]:
        	total_syllables_fifth_line += self.num_syllables(word)
        min_syllables = min(min_syllables, total_syllables_fifth_line)
        min_a_line_syllables = min(min_a_line_syllables, total_syllables_fifth_line)

        # print min_syllables, min_a_line_syllables, max_b_line_syllables
        # print total_syllables_first_line, total_syllables_second_line, total_syllables_third_line, total_syllables_fourth_line, total_syllables_fifth_line
        if min_syllables<4 or max_b_line_syllables>=min_a_line_syllables:
        	return False

        if abs(total_syllables_first_line - total_syllables_second_line)>2 or abs(total_syllables_first_line - total_syllables_fifth_line)>2 or abs(total_syllables_fifth_line - total_syllables_second_line)>2:
        	return False

        if abs(total_syllables_third_line - total_syllables_fourth_line)>2:
        	return False

        first_word = processed_text[0][-1]
        second_word = processed_text[1][-1]
        third_word = processed_text[2][-1]
        fourth_word = processed_text[3][-1]
        fifth_word = processed_text[4][-1]

        if self.rhymes(first_word, second_word) and self.rhymes(second_word, fifth_word) and self.rhymes(first_word, fifth_word) and self.rhymes(third_word, fourth_word):
        	if not self.rhymes(first_word, third_word) and not self.rhymes(second_word, third_word) and not self.rhymes(fifth_word, third_word):
        		if not self.rhymes(first_word, fourth_word) and not self.rhymes(second_word, fourth_word) and not self.rhymes(fifth_word, fourth_word):
        			return True

        return False

    def guess_syllables(self, word):
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

        print word, syllable_count
    	return syllable_count

    def apostrophe_tokenize(self, line):
    	line = line.strip().split()
    	new_line = list()

    	for word in line:
    		start_alpha = -1
    		end_alpha = -1

    		for i in range(len(word)):
    			if word[i].isalpha():
    				if start_alpha==-1:
    					start_alpha = i
    				else:
    					end_alpha = i

    		new_line += list(word[:start_alpha])
    		new_line.append(word[start_alpha:end_alpha+1])
    		new_line += list(word[end_alpha+1:])

    	return new_line

# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
