import pygame
from resources import *
from geometry import *
from engine import BaseCanvas
import time
import threading
import Queue

# Init pygame
pygame.init()

class InspirationEngine(BaseCanvas):
	def __init__(self, size = (1600, 950), caption = 'Inspiration Engine 0.1', max_fps = 40):
		BaseCanvas.__init__(self, size = size, caption = caption, max_fps = max_fps)

		self.img_queue = Queue.Queue()
		self.text_queue = Queue.Queue()

		self.spawn_area = (300, self.size[1])

	def _random_img(self):
		query = randomSentence((1, 3), 15000)
		self.text_queue.put(query)
		
		img = googleImage(query)
		if img:
			self.img_queue.put(img)

	def repeat_func(self):
		if not (self.tick)%150:
			# Fill the queue
			t = threading.Thread(target = self._random_img)
			t.setDaemon(True)
			t.start()
		
		# Empty the queue
		while not self.img_queue.empty():
			random_point = randomPoint(self.spawn_area, 140)
			self.add_image(self.img_queue.get(), random_point, 
				size_x = random.randrange(400, 500),
				moving = Point(random.randrange(15, 20)/10., 0),
				stay = 600, fade = 0)

		while not self.text_queue.empty():
			random_point = randomPoint((50, 100), 20)
			self.add_text(self.text_queue.get(), random_point,
				moving = Point(random.randrange(28, 40)/10., 0),
				stay = 600, fade = 0,
				color = (150, 10, 15)
				)
			
		return True

def main():
	canvas = InspirationEngine()

	# Start canvas animation
	canvas.start()

if __name__ == '__main__':
	main()
