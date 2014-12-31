# -*- coding: utf-8 -*-
"""Scrapes top rap artists and their top 100 tracks
"""
#url navigation/scraping
import urllib2
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from random import random

#run selenium headless
from pyvirtualdisplay import Display

#debugging
import ipdb as pdb

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
	return ''.join(s for s in text if ord(s)>31 and ord(s)<126)

"""
	Function which scrapes the top 388 rap albums' artist form Rate Your Music
"""
def get_rap_artists():
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
	Function which accepts an artists name and scrapes top 20 songs
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
def get_rap_lyrics(song_link):
	# we need to use selenium so the page actually populates
	driver = webdriver.Firefox()
	driver.get(song_link)
	driver.implicitly_wait(5)
	sleep(2*random()) # fake a human

	lyrics = driver.find_elements_by_class_name('lyrics')
	text = ""
	for lyric in lyrics:
		source = BeautifulSoup(lyric.get_attribute('innerHTML'))
		text += source.text
	text = raw_text(text)
	driver.close()
	pdb.set_trace()

get_rap_lyrics("http://genius.com/1858100/Public-enemy-fight-the-power/Yet-our-best-trained-best-educated-best-equipped-best-prepared-troops-refuse-to-fight-as-a-matter-of-fact-its-safe-to-say-that-they-would-rather-switch-than-fight")
