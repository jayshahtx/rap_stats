import os
import pdb
# store everything in a dictionary of dicts

# all_words = { word : word_dict }
# word_dict = { word : count }

#(TODO 1/23) - Choose words based on probability, not the one with the highest
#			 - Look into words in more than just pairs to identify the next


# step 1 - accept input of word  K and rapper M
# step 2 - look for every time the artist used the word K and what word came after
# step 3 - return the most popular result

def get_max(dic, prev_words):
	m = 0
	val = "NA"
	for key in dic.keys():
		if dic[key] > m and key not in prev_words:
			m = dic[key]
			val = key
	prev_words.append(val)
	return val, prev_words

def accept_word_and_rapper():
	"""Fn which accepts the word and rapper of interest from the user"""
	word = raw_input("Enter the word you're interested in: ")
	rapper = raw_input("Enter the rapper you're interested in: ")
	return word, rapper

def load_files(rapper):
	"""Fn which loads the text file with a rapper's lyrics, case 
		sensitive input"""
	path = os.path.abspath("lyrics/%s.txt" %rapper)
	lyrics = open(path, "r")
	text = lyrics.read()
	return text	

def look_for_words(lyrics, target, prev_words):
	"""Build markov chain of depth 2 and frequency count of each word"""
	next_words = {}
	lyrics = lyrics.split()
	for i in range(0,len(lyrics)-1):
		if target == lyrics[i]:
			next_words[lyrics[i+1]] = next_words.get(lyrics[i+1],0) + 1
	return get_max(next_words, prev_words)

def main():
	while True:
		i = 0
		target, rapper = accept_word_and_rapper()
		lyrics = load_files(rapper)

		prev_words = [] #keep track of words we've used already
		while i < 8:
			target, prev_words = look_for_words(lyrics, target, prev_words)
			print target
			i += 1
		print prev_words

main()