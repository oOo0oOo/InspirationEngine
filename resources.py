import time
from urllib import FancyURLopener
import urllib2
import simplejson

from pprint import pprint

def googleImage(search_term):
	'''
		Image search using Google Images inspired by: 
		http://stackoverflow.com/questions/11242967/python-search-with-image-google-images
	'''

	# construct url
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+search_term+'&start=0&userip=MyIP')
	print 'URL:', url
	request = urllib2.Request(url, None, {'Referer': 'testing'})
	response = urllib2.urlopen(request)

	# Get results using JSON
	results = simplejson.load(response)
	data = results['responseData']
	dataInfo = data['results']

	# Get image for three first results
	for image_url in dataInfo[:3]:
		pprint(image_url)



if __name__ == '__main__':

	# Define search term
	searchTerm = "Monkey Fork"

	# Replace spaces ' ' in search term for '%20' in order to comply with request
	searchTerm = searchTerm.replace(' ','%20')

	img = googleImage(searchTerm)
	print img
