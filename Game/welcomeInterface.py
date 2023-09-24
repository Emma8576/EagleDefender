import pygame
from pygame import *
import sys
import time
import tkinter as tk

window= tk.Tk()
init()
screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = display.set_mode((screen_width, screen_height), FULLSCREEN)
window.configure(cursor="star")                                     


volumen = 0.5
def iniciar():
    pygame.mixer.music.load('welcomeInterfaceFramesSprites/Sounds/mainSound1.mp3')
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)

# Iniciar automáticamente la configuración de volumen al ejecutar el juego
iniciar()

images = []
close = []

# Programar sprites ventana central
for i in range(1, 7):
    name = "welcomeInterfaceFramesSprites/mainItems/frame-"+str(i)+" (Custom).gif"
    images.append(image.load(name))

for i in range(1, 11):
    name1 = "welcomeInterfaceFramesSprites/mainItems1/frame-"+str(i)+".gif"
    close.append(image.load(name1))

def titleImage1():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/savedItems/title.png")
    picture = pygame.transform.scale(picture, [500,500])
    screen.blit(picture, [385,0])
def titleImage2():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/savedItems/mainDecoration.png")
    picture = pygame.transform.scale(picture, [470,470])
    screen.blit(picture, [395,240])

def titleImage3():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/savedItems/bottom.png")
    picture = pygame.transform.scale(picture, [300,60])
    screen.blit(picture, [0,660])

while True:
    for e in event.get():
        if e.type == QUIT: sys.exit()

    frame = int(time.time()*4)
    frame %= len(images)
    frame %= len(close)
    screen.fill((0, 0, 0))
    screen.blit(images[frame], (920,300))
    screen.blit(close[frame],(60,320))

    titleImage1()
    titleImage2()
    titleImage3()

    display.flip()
window.mainloop()
