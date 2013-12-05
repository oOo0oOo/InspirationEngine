import time
from threading import Thread

import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, K_DOWN

from geometry import *

# Init pygame
pygame.init()

# A Stoppable thread
class StoppableMultiExecThread(Thread): 
	def __init__ (self, target):
		Thread.__init__(self)
		self.target = target
		self.cont = True

	def run(self):
		while self.cont:
			res = self.target()
			if not res:
				self.cont = False
				return

	def stop(self):
		self.cont = False


class Canvas(Thread): 
	def __init__ (self):
		Thread.__init__(self)

		self.stop_flag = False

	def run(self):
		while not self.stop_flag:
			res = self.target()
			if not res:
				self.cont = False
				return

	def stop(self):
		self.stop_flag = True


class DisplayedObject(object):
	def __init__(self, position, moving = Point(0,0), rotation = 0, stay = 100, fade = 20):
		self.position = position
		self.moving = moving
		self.rotation = rotation
		self.stay = stay
		self.fade = fade

		self.age = 0

	def on_tick(self):
		self.age += 1
		self.position = self.position.transform(self.moving)

	def get_intensity(self):
		if self.age < self.stay:
			return 1.0
		elif self.age > self.stay + self.fade:
			return 0.0
		else:
			return round(float(self.fade) / (self.age - self.stay), 3)

class DisplayedImage(DisplayedObject):
	def __init__(self, image, position, moving = Point(0,0), rotation = 0, 
				stay = 100, fade = 20, size_x = False):

		DisplayedObject.__init__(self, position, moving = Point(0,0), 
				rotation = rotation, stay = stay, fade = fade)

		self.size_x = size_x
		self.image = image
		self.size = image.get_size()

	def on_tick(self):
		super(DisplayedImage, self).on_tick()

	def draw(self, window):
		if self.size_x:
			scale = float(self.size_x) / self.size[0]
		else:
			scale = 1
		# Rotozoom image
		rotated = pygame.transform.rotozoom(self.image, self.rotation, scale)

		#get the rect of the rotated surf and set it's center to the oldCenter
		rotRect = rotated.get_rect()
		rotRect.center = (self.position.x, self.position.y)
		window.blit(rotated, rotRect)
		return window

class BaseCanvas(object):
	def __init__(self, size = (1000, 800), caption = 'Python Canvas', max_fps = 40):
		# Setup some stuff
		self.max_fps = max_fps
		self.size = size
		self.fpsClock = pygame.time.Clock()
		self.window = pygame.display.set_mode(size)
		pygame.display.set_caption(caption)

		# some colors
		self.colors = {
			'white': pygame.Color(245, 245, 245),
			'brown': pygame.Color(133, 60, 8),
			'black': pygame.Color(5, 8, 7),
			'red': pygame.Color(255, 30, 30),
			'green': pygame.Color(28, 100, 22),
			'bright_green': pygame.Color(20, 245, 18),
			'blue': pygame.Color(5, 10, 145)
		}

		self.tick = 0
		self.displayed = []

	def repeat_func(self):
		'''
			Implement function in child class.
			Return False to stop Canvas.
		'''
		return True

	def start(self):
		while self.repeat_func():
			self.on_tick()
			self.fpsClock.tick(self.max_fps)

	def add_image(self, image, position, **args):
		self.displayed.append(DisplayedImage(image, position, **args))

	def close(self):
		pygame.quit()

	def on_tick(self):
		self.window.fill(self.colors['black'])

		# Draw all objects
		for o in self.displayed:
			o.draw(self.window)

		#Handle events (single press, not hold)
		for event in pygame.event.get():
			if event.type == QUIT:
				print 'QUIT'
				return False

		pygame.display.update()
		# Update state of all objects
		[o.on_tick() for o in self.displayed]

		self.tick += 1

class CanvasExample(BaseCanvas):
	def __init__(self, size = (1000, 800), caption = 'Python Canvas', max_fps = 40):
		BaseCanvas.__init__(self, size = size, caption = caption, max_fps = max_fps)

	def repeat_func(self):
		if not (self.tick+1)%150:
			return False
		return True


if __name__ == '__main__':
	canvas = CanvasExample()
	canvas.start()

