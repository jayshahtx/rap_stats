# file nav
import os
import sys

# scraping
from scraper.rap_scraper import get_top_songs
from scraper.rap_scraper import get_rap_link
from scraper.rap_scraper import get_rap_lyrics

# cleaning/organizing data
from counter.counter import get_count

# exporting/visualizing data
from visualizer.visualize import visualize, custom_data, graph_from_file

#misc
from time import sleep
import pickle
import pdb

def load_top_songs():
	f = open("songs.txt", "r")
	results = []
	for line in f:
		data = line.split(" !#! ")
		d = {}
		d['song'] = data[0]
		d['artist'] = data[1]
		d['year'] = data[2]
		results.append(d)
	return results

# save the block of text to disk
def save(name,text):
	path = os.path.abspath("lyrics/%s.txt" %name)
	text_file = open(path, "w")
	text_file.write(text.encode('utf-8'))
	text_file.close()

# get lyrics to top rap songs from 1989 to 2014
def scrape():
	#get all artists
	get_top_songs()
	results = load_top_songs()
	count = 0
	total = len(results)

	#get song lyrics
	for result in results:
		artist = result['artist']
		song = result['song']
		year = result['year']
		
		# try:
		print "\nScraping for %s, %s of %s"%(artist, count, total)
		
		#get all songs for artist
		song_link = get_rap_link(song, artist)

		# save lyrics if songs were actually found for this artist
		if song_link:
			
			#get all lyrics for song
			lyrics = get_rap_lyrics(song_link)

			#save the lyrics to disk
			save(year+"#"+song+"#"+artist,lyrics)

		else:
			print "\n%s not found in Rap Genius...skipping \n"%(artist)


		count+=1

def main():
	# scrape()
	# p_song_dict, p_year_dict = get_count("profanity")
	# f_song_dict, f_year_dict = get_count("female_names")
	# data = [p_song_dict, f_song_dict, p_year_dict]
	# pickle.dump(data, open("master_data_f_profanity.p", "wb"))

	# data = pickle.load(open("master_data_f_profanity.p", "rb"))
	# custom_data(data[1], data[0], data[2])

		# visualize(data[1], data[0], data[2])

	# csv = pickle.load(open("csv_of_data.p", "rb"))
	# from visualizer.visualize import graph
	graph_from_file()


if __name__ == '__main__':
	main()