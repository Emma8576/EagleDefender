import pygame
from pygame import *
import sys
import time

#hols
init()
screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = display.set_mode((screen_width, screen_height), FULLSCREEN)

images = []

#Programar sprites ventana central
for i in range(1, 7):
    name = "welcomeInterfaceFramesSprites/mainItems/frame-"+str(i)+" (Custom).gif"
    images.append(image.load(name))

def titleImage():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/mainWelcomeImages/mainTitle.png")
    picture = pygame.transform.scale(picture, [700,700])
    screen.blit(picture, [300,0])

while True:
    for e in event.get():
        if e.type == QUIT: sys.exit()


    frame = int(time.time()*10)
    frame %= len(images)
    screen.fill((255, 255, 255))
    screen.blit(images[frame], (800,400))

    titleImage()

    display.flip()
