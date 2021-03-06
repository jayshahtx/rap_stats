# -*- coding: utf-8 -*-
"""Scrapes top rap artists and their top 100 tracks
"""
#url scraping
from bs4 import BeautifulSoup
from selenium import webdriver

#url processing
import urllib2
import urllib
from time import sleep
from random import random
import re

#misc
from sets import Set

#debugging
import pdb


def hit_page(link):
	"""
	Function which accepts URL and returns BS object
	"""
	req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"}) 
	page = urllib2.urlopen( req )
	return BeautifulSoup(page)


def raw_text(text):
	"""
		Function which takes lyric text and strips of all formatting
	"""
	#make lower case
	# text = text.lower()
	#remove rap genius annotations
	text = re.sub(r'\[(.*)\]',"",text)
	#remove extra whitespace
	text = re.sub(r'\s\s+',' ',text)
	text = ' '.join(text.split())
	return text



def is_valid_artist(source):
	"""
		Function which checks the source of a page and determines if the artist
		exists in RapGenius' dataset or not
	"""
	results = source.find('h3',attrs={'class':'results_header'})
	# convert results to string object
	results = raw_text(results.get_text())
	# if the first word is 'results', that means no match occured
	if results[0] == 'results':
		return False
	else:
		return True

def is_right_song(source):
	"""
		Function which makes sure lyrics are of the right song
	"""
	pass


def get_top_songs():
	"""
		Function which scrapes the top rap singles from 1989-2013 from Wikipedia
		NOTE: The output is not perfect, but sufficient - manually verify output
	"""
	urls = [
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_1980s_and_1990s#1989",
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_2000s",
	"http://en.wikipedia.org/wiki/List_of_Billboard_Hot_Rap_Songs_number-one_hits_of_the_2010s"
	]

	results = []
	
	# go through each page
	for url in urls:
		source = hit_page(url)

		# get the table with all the artists
		rows = source.findAll('table')[2].findAll('tr')
		row_count = 1

		# hack to find the artists in a wikipedia table
		for row in rows[1:-1]:
			result = {}
			data = row.findAll('td')

			#find the song title
			song = row.find('th')
			if not song:
				song = data[0]
				song_title = song.text.encode('utf-8')
			else:
				song_title = song.text.encode('utf-8')

			song_title = song_title.split('[')[0] #remove brackets
			song_title = song_title.translate(None, '"') #remove quotations
			song_title = song_title.split(',')[0] #remove formatting errors
			result['song'] = song_title

			# find the artist
			cand1 = data[1].text.split(" featuring")[0].encode('utf-8')
			cand2 = data[0].text.split(" featuring")[0].encode('utf-8')
			if not cand1[-1].isalpha():
				artist = cand2
			else:
				artist = cand1
			artist = artist.split(',')[0]
			result['artist'] = artist


			# find the year
			date1 = data[2].text.encode('utf-8')
			date2 = data[1].text.encode('utf-8')
			if ',' in date1:
				date = date1[-4:]
			else:
				date = date2[-4:]
			result['year'] = date
			
			results.append(result)

	
	
	#write to disk to verify
	finalout = ""
	for result in results:
		s = result['song']
		a = result['artist']
		y = result['year']
		finalout += s + " !#! " + a + " !#! " + y + "\n"

	# text_file = open("songs.txt", "w")
	# text_file.write(finalout)
	# text_file.close()
	raw_input("Dumped output to songs.txt file, press enter after verifying data")


def get_rap_link(song, artist):
	"""
	Function which accepts an artists name and return URLs for top song
	"""
	url = "http://rap.genius.com/"
	target = url + "search?"
	params = urllib.urlencode({
		'q': artist + "-" + song
		})

	#get the source and check if its valid
	source = hit_page(target+params)
	try:
		if (is_valid_artist(source)):
			result = {}
			result['link'] = source.find('a', attrs={'class':' song_link'})['href']
			result['artist'] = artist
			result['song'] = song
			return result
	except:
		print "Error occured for %s - %s, skipping"%(artist, song)

		# links = source.findAll('a', attrs={'class':' song_link'})
		# max_songs = min(5,len(links))

		# # target_link = links[0]['href']
		# #find the URLs where the lyrics are located
		# lyric_links = []
		# for link in links[:max_songs]:
		# 	target = link['href']
		# 	lyric_links.append(target)

		# return lyric_links
	return None



def get_rap_lyrics(song_link_meta_data):
	"""
		Function which accepts a link to a song's page on rap genius and scrapes
		its lyrics in raw text
	"""
	out = ""
	driver = webdriver.PhantomJS()
		
	song_link  = song_link_meta_data['link']
	
	# use BS to get the song name and artist
	source = hit_page(song_link)
	song_name = raw_text(source.find(attrs={'class':'text_title'}).text)
	artist_name = raw_text(source.find(attrs={'class':'text_artist'}).text)

	# make sure we get the lyrics of the right song
	# if (artist_name not in song_link_meta_data['artist']) and \
	# 	(song_name not in song_link_meta_data['song']):
		
	# 	print "Could not match %s to %s"%(song_name, song_link_meta_data['song'])
	# 	return None

	#get the lyrics for each song
	# we need to use selenium so the page actually populates
	driver.get(song_link)
	driver.implicitly_wait(5)
	sleep(2*random()) # fake a human

	lyrics = driver.find_elements_by_class_name('lyrics')
	text = ""
	for lyric in lyrics:
		source = BeautifulSoup(lyric.get_attribute('innerHTML'))
		text += source.text
	text = raw_text(text)
	out += text

	driver.close()
	return out

def testing_func(url):
	source = hit_page(url)
	# check to see how many search results there are for this query
	results = source.find('h3',attrs={'class':'results_header'})
	# convert results to string object
	results = raw_text(results.get_text())
	# if the first word is 'Results', that means no match occured
	if results[0] == 'results':
		print "No match"
	else:
		print "Match"


		