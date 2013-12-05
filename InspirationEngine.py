import pygame
from resources import *
from geometry import *
from engine import BaseCanvas
import time

# Init pygame
pygame.init()

class InspirationEngine(BaseCanvas):
	def __init__(self, size = (1000, 800), caption = 'Inspiration Engine 0.1', max_fps = 40):
		self.size = size
		BaseCanvas.__init__(self, size = size, caption = caption, max_fps = max_fps)

	def repeat_func(self):
		if not (self.tick+1)%50:
			random_query = randomSentence()
			print random_query
			random_image = googleImage(random_query)
			random_point = randomPoint(self.size)
			self.add_image(googleImage(randomSentence()), random_point, size_x = random.randrange(100, 250))
			
		return True

def main():
	canvas = InspirationEngine()

	# Start canvas animation
	canvas.start()

if __name__ == '__main__':
	main()
