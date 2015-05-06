# file nav
import os
import sys

# scraping
from scraper.rap_scraper import get_top_songs
from scraper.rap_scraper import get_rap_link
from scraper.rap_scraper import get_rap_lyrics

#gender
from gender.gender import get_name_count


#misc
from time import sleep

import pdb

# save the block of text to disk
def save(name,text):
	path = os.path.abspath("lyrics/%s.txt" %name)
	text_file = open(path, "w")
	text_file.write(text.encode('utf-8'))
	text_file.close()

#scrape top 20 song lyrics for top 400 rap artists
def scrape():
	#get all artists
	results = get_top_songs()
	count = 0
	total = len(results)

	#get song lyrics
	for result in results:
		artist = result['artist']
		song = result['song']
		year = result['year']
		
		try:
			print "\nScraping for %s, %s of %s"%(artist, count, total)
			#get all songs for artist
			song_link = get_rap_link(result['song'], result['artist'])

			# save lyrics if songs were actually found for this artist
			if song_link:

				#get all lyrics for song
				lyrics = get_rap_lyrics(song_link)

				#save the lyrics to disk
				save(year+"-"+artist+"-"+song,lyrics)

			else:
				print "\n%s not found in Rap Genius...skipping \n"%(artist)

		except:
   			e = sys.exc_info()[0]
   			print "An error occured: %s"%(e)
   			sleep(10)


		count+=1

def count_female_refs():
	get_name_count()

def gender_count():
	pass

def main():
	# scrape()
	count_female_refs()

if __name__ == '__main__':
	main()