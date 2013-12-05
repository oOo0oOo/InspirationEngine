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
	print 'Word list (words.txt) not found. Will source externally from:'
	print word_site

	response = urllib2.urlopen(word_site)
	txt = simplejson.load(response)
	word_list = [a.keys()[0] for a in txt]

	# Save words.txt file
	open('words.txt','w+').write('\n'.join([w for w in word_list if len(w) > 3]))
	print 'Done... # Words (4 letters & more):', len(word_list)

def randomWord(most_popular = -1):
	if most_popular == -1 or 10 > most_popular or most_popular > len(word_list):
		return random.choice(word_list)
	else:
		return random.choice(word_list[10:most_popular])

def randomSentence(num = (1, 4), most_popular = -1):
	return ' '.join([randomWord(most_popular) for i in range(random.randrange(num[0], num[1]))])

def randomPoint(size = (1000, 800), border = 0):
	if not border:
		return Point(random.randrange(size[0]), random.randrange(size[1]))
	else:
		s0 = size[0] - 2 * border
		s1 = size[1] - 2 * border
		p = Point(random.randrange(s0), random.randrange(s1))
		return p.transform(Point(border, border))

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
	try:
		dataInfo = data['results']
	except TypeError, e:
		return False

	# return first result as pygame image
	file = False
	for url in dataInfo:
		# Only download small enough images
		if int(url['width']) < 1000 and int(url['height']) < 800:
			try:
				file = cStringIO.StringIO(urllib2.urlopen(url['url']).read())
				break
			except (urllib2.HTTPError, urllib2.URLError):
				pass

	if file:
		try:
			img =  pygame.image.load(file)
			return img
		except pygame.error:
			return False

	else:
		return False

if __name__ == '__main__':
	# Google Image with random search term
	img = googleImage(randomSentence())
