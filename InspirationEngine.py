import pygame
from resources import *
from geometry import *
import engine
import time

# Init pygame
pygame.init()

def main():
	canvas = engine.Canvas()

	# Add an image
	img1 = googleImage('Bread Castle')
	img2 = googleImage('Sun Blue')


	# Start canvas animation
	canvas.start()

	canvas.add_image(img1, Point(500, 400), size_x = 500, moving = Point(5, 5))
	canvas.add_image(img2, Point(250, 250), size_x = 300)

if __name__ == '__main__':
	main()
