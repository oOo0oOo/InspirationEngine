import pygame
import time

from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, K_DOWN
from geometry import *

# Init pygame
pygame.init()


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

		self.image = image
		self.size = image.get_size()
		if size_x:
			factor = float(size_x)/self.size[0]
			self.size = [s * factor for s in self.size]

	def on_tick(self):
		super(DisplayedObject, self).on_tick()

	def draw(self, window):
		scale = float(size_x) / self.size[0]
		# Rotozoom image
		rotated = pygame.transform.rotozoom(self.image, self.rotation, scale)

		#get the rect of the rotated surf and set it's center to the oldCenter
		rotRect = rotated.get_rect()
		point = point.transform(t_vect)
		rotRect.center = (point.x, point.y)

		window.blit(rotated, rotRect)

class Canvas(object):
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
		

		self.displayed = []

	def start(self):
		while True:
			self.on_tick()
			self.fpsClock.tick(self.max_fps)

	def add_image(self, image, position, **args):
		self.displayed.append(DisplayedImage(image, position, **args))

	def on_tick(self):

		self.window.fill(self.colors['black'])

		# Draw all objects
		[o.draw(self.window) for o in self.displayed]

		'''
					b1 = pygame.Rect(0, 0, general_params['border_size'], game_size[1])
					b2 = pygame.Rect(game_size[0] - general_params['border_size'], 0, general_params['border_size'], game_size[1])
					pygame.draw.rect(window, green, b1)
					pygame.draw.rect(window, green, b2)
				'''
		'''pygame.draw.line(window, white, (middle, m), (middle, m+80), 10)'''

		'''pygame.draw.circle(window, red, (int(point.x), int(y)), 1, 0)'''
		'''
			draw_text(str(dist_left) + 'm', Point(game_size[0] - general_params['border_size'], 60), 'helvetica', 25, white)
		'''
		#Handle events (single press, not hold)
		quitted = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quitted = True
			'''
			elif event.type == KEYDOWN and event.key == K_SPACE:
				game.board.pump()
			'''
		
		if not quitted:
			# Check for pressed leaning keys
			'''
				keys = pygame.key.get_pressed()
				if keys[K_LEFT]:
					game.board.lean(True)
				if keys[K_RIGHT]:
					game.board.lean(False)
				if keys[K_DOWN]:
					game.board.break_board()
			'''
			pygame.display.update()


			# Update state of all objects
			[o.on_tick() for o in self.displayed]

if __name__ == '__main__':
	canvas = Canvas()
	canvas.start_display()
