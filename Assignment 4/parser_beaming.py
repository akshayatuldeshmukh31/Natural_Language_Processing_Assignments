import sys, fileinput
from nltk.tree import Tree
from nltk.tokenize import TreebankWordTokenizer
import math
import re


# Parser modification - Beaming

kTOKENIZER = TreebankWordTokenizer()


def generate_string_parse_tree(parse_table, start, tokenized_text, sentence_length):
	stack = list()
	output = ""

	for i in range(len(parse_table[0][sentence_length-1][start][2])-1,-1,-1):
		stack.append([parse_table[0][sentence_length-1][start][2][i][0],parse_table[0][sentence_length-1][start][2][i][1],parse_table[0][sentence_length-1][start][2][i][2]])

	output = "(TOP { {)"

	while len(stack)!=0:

		current_node = stack[-1]
		del stack[-1]

		break_point = re.search('{', output).start()

		if current_node[1] != current_node[2]:
			output = output[:break_point] + "(" + current_node[0] + " { {)" + output[break_point + 1:]
			table_cell_value = parse_table[current_node[1]][current_node[2]]

			for cell in table_cell_value:
				if cell[0] == current_node[0]:
					for i in range(len(cell[2])-1,-1,-1):
						stack.append([cell[2][i][0],cell[2][i][1],cell[2][i][2]])
					break

		if current_node[1] == current_node[2]:
			output = output[:break_point] + "(" + current_node[0] + " " + tokenized_text[current_node[1]] + ")" + output[break_point + 1:]

	return output

# grammar_rules -> Hashtable (Key - RHS, Value - [(LHS, Prob)])
# Table cell value [LHS Head, Prob, [[RHS part, H_row, H_col], [RHS part, V_row, V_col]]]
# Entry - [LHS, Prob] 

def parse_sentence(grammar_rules, prior_probabilities, sentence):

	# print grammar_rules
	tokenized_text = kTOKENIZER.tokenize(sentence)
	length_tokenized_text = len(tokenized_text)
	parse_table = []
	beaming_array = []

	for i in range(len(tokenized_text)):
		parse_table.append([None for x in range(len(tokenized_text))])

	for l in range(length_tokenized_text):
		for i in range(length_tokenized_text):
			
			if (i+l)>=length_tokenized_text:
				continue

			parse_table[i][i+l] = []

			if l==0:
				token = "'" + tokenized_text[i+l] + "'"

				if grammar_rules.get(token, -1)==-1:
					token = "'<unk>'"

				entries = grammar_rules[token]

				for entry in entries:

					flag = 0
						
					for cell_num in range(len(parse_table[i][i+l])):
						if parse_table[i][i+l][cell_num][0] == entry[0]:
							flag = 1
							if parse_table[i][i+l][cell_num][1] < entry[1]:
								parse_table[i][i+l][cell_num][1] = entry[1]

					if flag == 0:
						parse_table[i][i+l].append([entry[0], entry[1], [[None, None, None], [None, None, None]]])

				# print ""
				# print i,i+l
				# print parse_table[i][i+l]

			else:

				for k in range(i,i+l):

					table_cell_value_1 = parse_table[i][k]
					table_cell_value_2 = parse_table[k+1][i+l]

					for cell_value_1 in range(len(table_cell_value_1)):
						for cell_value_2 in range(len(table_cell_value_2)):

							token = table_cell_value_1[cell_value_1][0] + " " + table_cell_value_2[cell_value_2][0]
							
							if grammar_rules.get(token, -1)==-1:
								continue

							entries = grammar_rules[token]

							for entry in entries:

								flag = 0

								for table_cell_value in parse_table[i][i+l]:
									if table_cell_value[0] == entry[0]:
										flag = 1
										if table_cell_value[1] < (entry[1] + table_cell_value_1[cell_value_1][1] + table_cell_value_2[cell_value_2][1]):
											table_cell_value[1] = entry[1] + table_cell_value_1[cell_value_1][1] + table_cell_value_2[cell_value_2][1]
											table_cell_value[2] = [[table_cell_value_1[cell_value_1][0], i, k], [table_cell_value_2[cell_value_2][0], k+1, i+l]]

								if flag == 0:
									parse_table[i][i+l].append([entry[0], entry[1] + table_cell_value_1[cell_value_1][1] + table_cell_value_2[cell_value_2][1], [[table_cell_value_1[cell_value_1][0], i, k], [table_cell_value_2[cell_value_2][0], k+1, i+l]]])


				if len(parse_table[i][i+l])!=0:

					omissions = int(math.floor(len(parse_table[i][i+l])*0.15))

					for c in range(len(parse_table[i][i+l])):
						beaming_array.append([parse_table[i][i+l][c][0], parse_table[i][i+l][c][1]])

					for c in range(len(beaming_array)):
						if prior_probabilities.get(beaming_array[c][0], -1)!=-1:
							beaming_array[c][1] = beaming_array[c][1] + prior_probabilities[beaming_array[c][0]]
						else:
							beaming_array[c][1] = 0.0

					beaming_array.sort(key=lambda x: x[1])

					for c in range(omissions):
						for d in range(len(parse_table[i][i+l])):
							if beaming_array[c][0] == parse_table[i][i+l][d][0]:
								del parse_table[i][i+l][d]
								break

	
	# Generate string form of the parse tree
	flag = 0
	position = 0

	for i in range(len(parse_table[0][length_tokenized_text-1])):
		if parse_table[0][length_tokenized_text-1][i][0] == 'TOP':
			flag = 1
			position = i
			break

	if flag == 0:
		return tuple(("",0))
	else:
		return tuple((generate_string_parse_tree(parse_table, position, tokenized_text, length_tokenized_text), parse_table[0][length_tokenized_text-1][position][1]))