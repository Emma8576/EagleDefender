import pygame
from pygame import *
import sys
import time

init()

screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = display.set_mode((screen_width, screen_height), FULLSCREEN)

images = []
images_left = []
images_right = []



#Programar sprites ventana central
for i in range(1, 14):
    name = "welcomeInterfaceFramesSprites/mainWelcome/frame-"+str(i)+".gif"
    images.append(image.load(name))

#Programar sprites lateral izquieda
for i in range(1,19):
    name_left = "welcomeInterfaceFramesSprites/secondWelcome/frame-" + str(i) + ".gif"
    images_left.append(image.load(name_left))

    name_right = "welcomeInterfaceFramesSprites/secondWelcome/frame-" + str(i) + ".gif"
    images_right.append(image.load(name_right))

def titleImage():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/mainWelcomeImages/mainTitle.png")
    picture = pygame.transform.scale(picture, [500,500])
    screen.blit(picture, [380,50])

while True:
    for e in event.get():
        if e.type == QUIT: sys.exit()

    frame = int(time.time()*10)
    frame %= len(images)

    screen.fill((255, 255, 255))

    screen.blit(images[frame], (280,10))
    screen.blit(images_left[frame],(-69,10))
    screen.blit(images_right[frame], (980, 10))

    titleImage()

    display.flip()
