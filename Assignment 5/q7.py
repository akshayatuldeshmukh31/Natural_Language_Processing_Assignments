import distsim, fileinput
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

# Entry - [Category, Size, 1-best, 5-best, 10-best]
categories_n_best_data = list()
incorrect_data = list()

for line in fileinput.input():
	if line[0]==":":
		categories_n_best_data.append([line.strip().split()[1], 0.0, 0.0, 0.0, 0.0])
		incorrect_data.append([line.strip().split()[1]])
		incorrect_entry_flag = 0
		print line.strip().split()[1]
	elif line[0].isalpha() or line[0].isdigit():

		categories_n_best_data[-1][1] += 1

		words = line.strip().split()
		vec_w1 = word_to_vec_dict[words[0]]
		vec_w2 = word_to_vec_dict[words[1]]
		vec_w4 = word_to_vec_dict[words[3]]

		return_tuples = distsim.show_nearest(word_to_vec_dict,
                           vec_w1-vec_w2+vec_w4,
                           set([words[0],words[1],words[3]]),
                           distsim.cossim_dense)

		flag = 0

		# 1-best
		if return_tuples[0][0]==words[2]:
			categories_n_best_data[-1][2] += 1
			flag = 1

		# 5-best
		length = 0

		if len(return_tuples)>=5:
			length = 5
		else:
			length = len(return_tuples)

		for i in range(length):
			if return_tuples[i][0]==words[2]:
				categories_n_best_data[-1][3] += 1
				flag = 1
				break

		# 10-best
		for i in range(len(return_tuples)):
			if return_tuples[i][0]==words[2]:
				categories_n_best_data[-1][4] += 1
				flag = 1
				break

		if flag==0 and incorrect_entry_flag==0:
			incorrect_data[-1].append(words)
			incorrect_data[-1].append(return_tuples)
			incorrect_entry_flag = 1
			

print "*** DATA ***"
for i in range(len(categories_n_best_data)):
	if categories_n_best_data[i][1]!=0:
		categories_n_best_data[i][2] = float(categories_n_best_data[i][2])/float(categories_n_best_data[i][1])
		categories_n_best_data[i][3] = float(categories_n_best_data[i][3])/float(categories_n_best_data[i][1])
		categories_n_best_data[i][4] = float(categories_n_best_data[i][4])/float(categories_n_best_data[i][1])
	print "CATEGORY: ", categories_n_best_data[i][0]
	print "1-BEST: ", categories_n_best_data[i][2]
	print "5-BEST: ", categories_n_best_data[i][3]
	print "10-BEST: ", categories_n_best_data[i][4]
	print ""

print ""
print "*** INCORRECT DATA ***"

for i in range(len(incorrect_data)):
	if len(incorrect_data[i])>1:
		print "CATEGORY: ", incorrect_data[i][0]
		print "WORDS: ", incorrect_data[i][1]
		print "TUPLES: ", incorrect_data[i][2]
		print ""
