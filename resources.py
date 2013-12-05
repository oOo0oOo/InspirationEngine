import time
import pygame
import random
from urllib import FancyURLopener
import urllib2
import simplejson
from geometry import Point

import cStringIO

#init pygame
pygame.init()

# Load word list
# try saved file
try:
	local_file = "words.txt"
	word_list = open(local_file).read().splitlines()

# If file not found, source external resource
except IOError, e:
	word_site = 'http://www.alexdadgar.com/projects/rank/api?top=5000'
	response = urllib2.urlopen(word_site)
	txt = simplejson.load(response)
	word_list = [a.keys()[0] for a in txt]

	# Save words.txt file
	open('words.txt','w+').write('\n'.join(word_list))

def randomWord():
	return random.choice(word_list)

def randomSentence(num = (1, 4)):
	return ' '.join([randomWord() for i in range(random.randrange(num[0], num[1]))])

def randomPoint(size = (1000, 800)):
	return Point(random.randrange(size[0]), random.randrange(size[0]))

def googleImage(search_term):
	'''
		Image search using Google Images inspired by: 
		http://stackoverflow.com/questions/11242967/python-search-with-image-google-images
	'''
	# Replace spaces ' ' in search term for '%20' in order to comply with request
	search_term = search_term.replace(' ','%20')

	# construct url
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+search_term+'&start=0&userip=MyIP')
	request = urllib2.Request(url, None, {'Referer': 'testing'})
	response = urllib2.urlopen(request)

	# Get results using JSON
	results = simplejson.load(response)
	data = results['responseData']
	dataInfo = data['results']

	# return first result as pygame image
	for url in dataInfo:
		img_url = url['url']
		try:
			file = cStringIO.StringIO(urllib2.urlopen(img_url).read())
			break
		except urllib2.HTTPError, e:
			pass
	
	return pygame.image.load(file)

if __name__ == '__main__':
	# Google Image with random search term
	img = googleImage(randomSentence())
