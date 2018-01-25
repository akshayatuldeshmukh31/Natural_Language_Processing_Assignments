import sys, fileinput
from nltk.tree import Tree
from parser import parse_sentence
import math

grammar_rules = dict()
rules_list = fileinput.input("pcfg.rules")

flag = 0

for line in rules_list:
	line = line.strip()

	if len(line)==0:
		continue

	split_lines = line.split("#")
	split_lines[0] = split_lines[0].strip()
	rule_prob = float(split_lines[1].strip())

	rule_body = split_lines[0].split("->")
	rule_body[0] = rule_body[0].strip()
	rule_body[1] = rule_body[1].strip()

	if grammar_rules.get(rule_body[1], -1)==-1:
		grammar_rules[rule_body[1]] = []
	grammar_rules[rule_body[1]].append(tuple((rule_body[0], math.log(rule_prob, 10))))

for line in fileinput.input():
	if(len(line)==0):
		continue

	print parse_sentence(grammar_rules, line.strip())[0]
		