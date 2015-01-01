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
	Function which scrapes the top 388 rap albums' artist form Rate Your Music
"""
def get_rap_artists_old():
	url = "http://rateyourmusic.com/list/ChrisPC/the_500_greatest_hip_hop_albums__plus_the_other_ones_that_are_honorable_mention_/"
	results = []

	#get results from all the pages
	for i in range(0,4): 
		temp_url = url + str(i) + "/"
		source = hit_page(temp_url)	
		artists = source.findAll("h4") #hack to ignore the first element
		for a in artists[1:-1]:
			results.append(str(a.text.encode('utf-8'))) #convert to utf for comprehension
	return results


"""
	Function which scrapes the top rap artists from 1989-2013 from Wikipedia
	NOTE: The output is not perfect
"""
def get_rap_artists():
	urls = [
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_1980s_and_1990s#1989",
	"http://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_2000s",
	"http://en.wikipedia.org/wiki/List_of_Billboard_Hot_Rap_Songs_number-one_hits_of_the_2010s"
	]

	artists = []
	
	# go through each page
	for url in urls:
		source = hit_page(url)
		# get the table with all the artists
		rows = source.findAll('table')[2].findAll('tr')
		row_count = 1

		# hack to find the artists in a wikipedia table
		while row_count < len(rows):
			data = rows[row_count].findAll('td')
			if row_count == 1:
				artists.append(data[1].text.split(" featuring")[0])
			else:
				artists.append(data[0].text.split(" featuring")[0])
			row_count += 1
	
	#write to disk
	text_file = open("artists.txt", "w")
	for artist in artists:
		text_file.write(artist.encode('utf-8') + "\n")
	text_file.close()

"""
	Function which accepts an artists name and return URLs for top 20 songs
"""
def get_rap_songs(artist):
	url = "http://rap.genius.com/"
	target = url + "search?"
	params = urllib.urlencode({
		'q':artist
		})
	source = hit_page(target+params)
	links = source.findAll('a', attrs={'class':' song_link'})

	#find the URLs where the lyrics are located
	lyric_links = []
	for link in links:
		target = link['href']
		lyric_links.append(target)

	return lyric_links


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
		