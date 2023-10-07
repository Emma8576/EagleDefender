import pygame
import sys

pygame.init()


clock = pygame.time.Clock()

size = (1980,1080)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

background = pygame.image.load("panel_elements/bg/bg (1).png").convert()

while True:
	screen.blit(background,[0,0])
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			sys.exit()

	pygame.display.flip()
	clock.tick(60)

pygame.quit()

