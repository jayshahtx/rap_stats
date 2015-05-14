# file nav
import os
import sys

# scraping
from scraper.rap_scraper import get_top_songs
from scraper.rap_scraper import get_rap_links
from scraper.rap_scraper import get_rap_lyrics

#gender
from counter.counter import get_count


#misc
from time import sleep

import pdb

# save the block of text to disk
def save(name,text):
	path = os.path.abspath("lyrics/%s.txt" %name)
	text_file = open(path, "w")
	text_file.write(text.encode('utf-8'))
	text_file.close()

# get lyrics to top rap songs from 1989-2014
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
			song_links = get_rap_links(result['song'], result['artist'])

			# save lyrics if songs were actually found for this artist
			if song_links:
				
				#get all lyrics for song
				lyrics = get_rap_lyrics(song_links)

				#save the lyrics to disk
				save(year+"-"+artist,lyrics)

			else:
				print "\n%s not found in Rap Genius...skipping \n"%(artist)

		except:
   			e = sys.exc_info()[0]
   			print "An error occured: %s"%(e)
   			sleep(10)


		count+=1

def main():
	scrape()
	# get_count("female_names")

if __name__ == '__main__':
	main()