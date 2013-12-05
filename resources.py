import time
import random
from urllib import FancyURLopener
import urllib2
import simplejson

from pprint import pprint

# Load word list
# try saved file
try:
	local_file = "words.txt"
	word_list = open(local_file).read().splitlines()

# If file not found, source external resource
except IOError, e:
	word_site = "http://www.freebsd.org/cgi/cvsweb.cgi/src/share/dict/web2?rev=1.12;content-type=text%2Fplain"

	response = urllib2.urlopen(word_site)
	txt = response.read()
	word_list = txt.splitlines()

	# Save words.txt file
	open('words.txt','w+').write(txt)

def randomWord():
	return random.choice(word_list)

def googleImage(search_term):
	'''
		Image search using Google Images inspired by: 
		http://stackoverflow.com/questions/11242967/python-search-with-image-google-images
	'''

	# construct url
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+search_term+'&start=0&userip=MyIP')
	# print 'URL:', url
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
	searchTerm = ' '.join([randomWord() for i in range(random.randrange(1, 3))])

	print searchTerm

	# Replace spaces ' ' in search term for '%20' in order to comply with request
	searchTerm = searchTerm.replace(' ','%20')

	print searchTerm

	img = googleImage(searchTerm)
	print img
