import pygame
import sys
from pygame import *
import time


pygame.init()

screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = display.set_mode((screen_width, screen_height), FULLSCREEN)


clock = pygame.time.Clock()

bg = []

for i in range(1,24):
	nombre_bg="panel_elements/bg/frame-"+str(i)+".gif"
	bg.append(image.load(nombre_bg))


while True:
	screen.fill((255,0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			sys.exit()

	frame = int(time.time()*10)
	frame %= len(bg)

	screen.blit(bg[frame],(0,0))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()

