import sys, fileinput
from nltk.tree import Tree
from parser_HM import parse_sentence
import math

grammar_rules = dict()
prior_probabilities = dict()
total_rules = 0
rules_list = fileinput.input("pcfg_HM.rules")

flag = 0

for line in rules_list:
	line = line.strip()

	if len(line)==0:
		continue

	total_rules += 1
	split_lines = line.split("#")
	split_lines[0] = split_lines[0].strip()
	rule_prob = float(split_lines[1].strip())

	rule_body = split_lines[0].split("->")
	rule_body[0] = rule_body[0].strip()
	rule_body[1] = rule_body[1].strip().split()

	if grammar_rules.get(" ".join(rule_body[1]), -1)==-1:
		grammar_rules[" ".join(rule_body[1])] = []
	grammar_rules[" ".join(rule_body[1])].append(tuple((rule_body[0], math.log(rule_prob, 10))))

	if prior_probabilities.get(rule_body[0], -1)==-1:
		prior_probabilities[rule_body[0]] = 0
	prior_probabilities[rule_body[0]] += 1

for key,value in prior_probabilities.items():
	prior_probabilities[key] = math.log(float(prior_probabilities[key])/float(total_rules), 10)

for line in fileinput.input():
	if(len(line)==0):
		continue

	print parse_sentence(grammar_rules, prior_probabilities, line.strip())[0]
	# break