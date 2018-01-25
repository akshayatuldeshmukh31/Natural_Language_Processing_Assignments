import sys, fileinput
from nltk.tree import Tree

cfg_rules_dict = dict()
cfg_literal_count_dict = dict()

for line in fileinput.input():
	t = Tree.fromstring(line.strip())
	list_of_rules = t.productions()

	for rule in list_of_rules:
		if cfg_rules_dict.get(rule, -1)==-1:
			cfg_rules_dict[rule] = 0
		if cfg_literal_count_dict.get(rule.lhs(), -1)==-1:
			cfg_literal_count_dict[rule.lhs()] = 0
		cfg_rules_dict[rule] += 1
		cfg_literal_count_dict[rule.lhs()] += 1

max_frequent = 0
max_frequent_rule = None

for key, value in sorted(cfg_rules_dict.items()):
	prob = float(value)/float(cfg_literal_count_dict[key.lhs()])

	if(max_frequent < value):
		max_frequent = value
		max_frequent_rule = key

	print str(key).strip(),"#",str(prob)

# print "\nMAX_FREQ",str(max_frequent_rule),str(max_frequent)