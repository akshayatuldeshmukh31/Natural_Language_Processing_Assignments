import sys, fileinput
from nltk.tree import Tree
import collections

cfg_rules_dict = dict()
cfg_literal_count_dict = dict()
stack = list()

for line in fileinput.input():
	t = Tree.fromstring(line.strip())
	list_of_rules = t.productions()
	del stack[:]

	for rule in list_of_rules:
		
		# print "STACK",stack

		str_rule = str(rule).strip().split("->")
		str_rule[0] = str_rule[0].strip()
		str_rule[1] = str_rule[1].strip().split()
		# print str_rule[1]
		
		if len(stack)!=0:
			if str_rule[0] == stack[-1][0]:
				str_rule[0] = str_rule[0] + "^" + stack[-1][1]
				del stack[-1]

		if len(str_rule[1])==2:
			stack.append(tuple((str_rule[1][1], str_rule[1][0])))
			str_rule[1][1] = str_rule[1][1] + "^" + str_rule[1][0]

		new_rule = " -> ".join([str_rule[0], " ".join(str_rule[1])])
		# print new_rule

		if cfg_rules_dict.get(new_rule, -1)==-1:
			cfg_rules_dict[new_rule] = 0
		if cfg_literal_count_dict.get(str_rule[0], -1)==-1:
			cfg_literal_count_dict[str_rule[0]] = 0
		cfg_rules_dict[new_rule] += 1
		cfg_literal_count_dict[str_rule[0]] += 1

		# for literal in rule.rhs():
		# 	if cfg_literal_count_dict.get(literal, -1)==-1:
		# 		cfg_literal_count_dict[literal] = 0
		# 	cfg_literal_count_dict[literal] += 1

	# break

# max_frequent = 0
# max_frequent_rule = None

for key, value in sorted(cfg_rules_dict.items()):
	prob = float(value)/float(cfg_literal_count_dict[key.strip().split("->")[0].strip()])

	# if(max_frequent < value):
	# 	max_frequent = value
		# max_frequent_rule = key

	print str(key).strip(),"#",str(prob)

# print "\nMAX_FREQ",str(max_frequent_rule),str(max_frequent)