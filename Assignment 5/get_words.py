import distsim, fileinput
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")

for key,value in word_to_vec_dict.items():
	print key