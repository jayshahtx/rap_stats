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

"""
	Function which accepts URL and returns BS object
"""
def hit_page(link):
	req = urllib2.Request(link, headers={'User-Agent' : "Magic Browser"}) 
	page = urllib2.urlopen( req )
	return BeautifulSoup(page)

"""
	Function which takes lyric text and strips of all formatting
"""
def raw_text(text):
	#make lower case
	text = text.lower()
	#remove rap genius annotations
	text = re.sub(r'\[(.*)\]',"",text)
	#remove extra whitespace
	text = re.sub(r'\s\s+',' ',text)
	text = ' '.join(text.split())
	return text


"""
	Function which checks the source of a page and determines if the artist
	exists in RapGenius' dataset or not
"""
def is_valid_artist(source):
	results = source.find('h3',attrs={'class':'results_header'})
	# convert results to string object
	results = raw_text(results.get_text())
	# if the first word is 'results', that means no match occured
	if results[0] == 'results':
		return False
	else:
		return True

"""
	Function which scrapes the top rap artists from 1989-2013 from Wikipedia
	NOTE: The output is not perfect, but sufficient - manually verify output
"""
def get_rap_artists():
	urls = [
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_1980s_and_1990s#1989",
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_2000s",
	"http://en.wikipedia.org/wiki/List_of_Billboard_Hot_Rap_Songs_number-one_hits_of_the_2010s"
	]

	artists = Set([])
	
	# go through each page
	for url in urls:
		source = hit_page(url)

		# get the table with all the artists
		rows = source.findAll('table')[2].findAll('tr')
		row_count = 1

		# hack to find the artists in a wikipedia table
		for row in rows[1:-1]:
			data = row.findAll('td')
			# there are two places the artist name could be stored
			cand1 = data[1].text.split(" featuring")[0].encode('utf-8')
			cand2 = data[0].text.split(" featuring")[0].encode('utf-8')
	
			# easy way to identify which one
			if not cand1[-1].isalpha():
				artists.add(cand2)
			else:
				artists.add(cand1)

	
	#write to disk to verify
	text_file = open("artists.txt", "w")
	for artist in artists:
		text_file.write(artist + "\n")
	text_file.close()

	return artists

"""
	Function which accepts an artists name and return URLs for top 20 songs
"""
def get_rap_songs(artist):
	url = "http://rap.genius.com/"
	target = url + "search?"
	params = urllib.urlencode({
		'q':artist
		})

	#get the source and check if its valid
	source = hit_page(target+params)
	
	if (is_valid_artist(source)):
		links = source.findAll('a', attrs={'class':' song_link'})

		#find the URLs where the lyrics are located
		lyric_links = []
		for link in links:
			target = link['href']
			lyric_links.append(target)

		return lyric_links
	return None


"""
	Function which accepts a link to a song's page on rap genius and scrapes
	its lyrics in raw text
"""
def get_rap_lyrics(song_links):
	out = ""
	driver = webdriver.Firefox()
	
	#get the lyrics for each song
	for song_link in song_links:
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


		