import time
import pygame
from urllib import FancyURLopener
import urllib2
import simplejson

import cStringIO

#init pygame
pygame.init()

def googleImage(search_term):
	'''
		Image search using Google Images inspired by: 
		http://stackoverflow.com/questions/11242967/python-search-with-image-google-images
	'''
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
	# Define search term
	searchTerm = "Monkey Fork"
	print googleImage(searchTerm)
