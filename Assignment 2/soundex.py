from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
	"""
	Returns an FST that converts letters to numbers as specified by
	the soundex algorithm
	"""

	# Let's define our first FST
	f1 = FST('soundex-generate')

	# Indicate that '1' is the initial state
	f1.add_state('start')
	f1.add_state('group1')
	f1.add_state('group2')
	f1.add_state('group3')
	f1.add_state('group4')
	f1.add_state('group5')
	f1.add_state('group6')
	f1.add_state('group0')
	f1.initial_state = 'start'

	# Set all the final states
	f1.set_final('group1')
	f1.set_final('group2')
	f1.set_final('group3')
	f1.set_final('group4')
	f1.set_final('group5')
	f1.set_final('group6')
	f1.set_final('group0')

	# Add the rest of the arcs
	for letter in string.letters:

		if letter in ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']:
			f1.add_arc('start', 'group1', (letter), (letter))
			f1.add_arc('group1', 'group1', (letter), (''))

			f1.add_arc('group0', 'group1', (letter), ('1'))
			f1.add_arc('group2', 'group1', (letter), ('1'))
			f1.add_arc('group3', 'group1', (letter), ('1'))
			f1.add_arc('group4', 'group1', (letter), ('1'))
			f1.add_arc('group5', 'group1', (letter), ('1'))
			f1.add_arc('group6', 'group1', (letter), ('1'))

		elif letter in ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']:
			f1.add_arc('start', 'group2', (letter), (letter))
			f1.add_arc('group2', 'group2', (letter), (''))

			f1.add_arc('group0', 'group2', (letter), ('2'))
			f1.add_arc('group1', 'group2', (letter), ('2'))
			f1.add_arc('group3', 'group2', (letter), ('2'))
			f1.add_arc('group4', 'group2', (letter), ('2'))
			f1.add_arc('group5', 'group2', (letter), ('2'))
			f1.add_arc('group6', 'group2', (letter), ('2'))

		elif letter in ['d', 't', 'D', 'T']:
			f1.add_arc('start', 'group3', (letter), (letter))
			f1.add_arc('group3', 'group3', (letter), (''))

			f1.add_arc('group0', 'group3', (letter), ('3'))
			f1.add_arc('group1', 'group3', (letter), ('3'))
			f1.add_arc('group2', 'group3', (letter), ('3'))
			f1.add_arc('group4', 'group3', (letter), ('3'))
			f1.add_arc('group5', 'group3', (letter), ('3'))
			f1.add_arc('group6', 'group3', (letter), ('3'))

		elif letter in ['l', 'L']:
			f1.add_arc('start', 'group4', (letter), (letter))
			f1.add_arc('group4', 'group4', (letter), (''))

			f1.add_arc('group0', 'group4', (letter), ('4'))
			f1.add_arc('group1', 'group4', (letter), ('4'))
			f1.add_arc('group2', 'group4', (letter), ('4'))
			f1.add_arc('group3', 'group4', (letter), ('4'))
			f1.add_arc('group5', 'group4', (letter), ('4'))
			f1.add_arc('group6', 'group4', (letter), ('4'))

		elif letter in ['m', 'n', 'M', 'N']:
			f1.add_arc('start', 'group5', (letter), (letter))
			f1.add_arc('group5', 'group5', (letter), (''))

			f1.add_arc('group0', 'group5', (letter), ('5'))
			f1.add_arc('group1', 'group5', (letter), ('5'))
			f1.add_arc('group2', 'group5', (letter), ('5'))
			f1.add_arc('group3', 'group5', (letter), ('5'))
			f1.add_arc('group4', 'group5', (letter), ('5'))
			f1.add_arc('group6', 'group5', (letter), ('5'))

		elif letter in ['r', 'R']:
			f1.add_arc('start', 'group6', (letter), (letter))
			f1.add_arc('group6', 'group6', (letter), (''))

			f1.add_arc('group0', 'group6', (letter), ('6'))
			f1.add_arc('group1', 'group6', (letter), ('6'))
			f1.add_arc('group2', 'group6', (letter), ('6'))
			f1.add_arc('group3', 'group6', (letter), ('6'))
			f1.add_arc('group4', 'group6', (letter), ('6'))
			f1.add_arc('group5', 'group6', (letter), ('6'))

		else:
			f1.add_arc('start', 'group0', (letter), (letter))
			f1.add_arc('group0', 'group0', (letter), (''))

			f1.add_arc('group1', 'group0', (letter), (''))
			f1.add_arc('group2', 'group0', (letter), (''))
			f1.add_arc('group3', 'group0', (letter), (''))
			f1.add_arc('group4', 'group0', (letter), (''))
			f1.add_arc('group5', 'group0', (letter), (''))
			f1.add_arc('group6', 'group0', (letter), (''))

	return f1

	# The stub code above converts all letters except the first into '0'.
	# How can you change it to do the right conversion?

def truncate_to_three_digits():
	"""
	Create an FST that will truncate a soundex string to three digits
	"""

	# Ok so now let's do the second FST, the one that will truncate
	# the number of digits to 3
	f2 = FST('soundex-truncate')

	# Indicate initial and final states
	f2.add_state('1')
	f2.add_state('2')
	f2.add_state('3')
	f2.add_state('4')
	f2.initial_state = '1'
	f2.set_final('2')
	f2.set_final('3')
	f2.set_final('4')

	# Add the arcs
	for letter in string.letters:
		f2.add_arc('1', '1', (letter), (letter))

	for n in range(6):
		f2.add_arc('1', '2', (str(n+1)), (str(n+1)))
		f2.add_arc('2', '3', (str(n+1)), (str(n+1)))
		f2.add_arc('3', '4', (str(n+1)), (str(n+1)))
		f2.add_arc('4', '4', (str(n+1)), ())

	return f2

	# The above stub code doesn't do any truncating at all -- it passes letter and number input through
	# what changes would make it truncate digits to 3?

def add_zero_padding():
	# Now, the third fst - the zero-padding fst
	f3 = FST('soundex-padzero')

	f3.add_state('1')
	f3.add_state('2')
	f3.add_state('3')
	f3.add_state('4')
	
	f3.initial_state = '1'
	f3.set_final('4')

	f3.add_arc('1', '2', (''), ('0'))
	f3.add_arc('2', '3', (''), ('0'))
	f3.add_arc('3', '4', (''), ('0'))
	
	for letter in string.letters:
		f3.add_arc('1', '1', (letter), (letter))
	for number in xrange(6):
		f3.add_arc('1', '2', (str(number+1)), (str(number+1)))
		f3.add_arc('2', '3', (str(number+1)), (str(number+1)))
		f3.add_arc('3', '4', (str(number+1)), (str(number+1)))
	
	return f3

	# The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
	user_input = raw_input().strip()
	f1 = letters_to_numbers()
	f2 = truncate_to_three_digits()
	f3 = add_zero_padding()

	if user_input:
		print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
