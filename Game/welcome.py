import pygame
from pygame import *
import sys
import time
import tkinter as tk
import os
import msvcrt
import subprocess

init()
screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = display.set_mode((screen_width, screen_height), FULLSCREEN)
window = tk.Tk()
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

def abrir_login():
    subprocess.Popen(["python", "Login.py"])

def titleImage1():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/savedItems/title.png")
    picture = pygame.transform.scale(picture, [550,200])
    screen.blit(picture, [370,520])

def salir():
    window.destroy()

def check_click(image_rect1, image_rect2):
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:  # Verifica clic izquierdo
            mouse_pos = pygame.mouse.get_pos()
            if image_rect1.collidepoint(mouse_pos):
                print("Clic izquierdo en el botón!")
                abrir_login()  # Abre Login.py
            if image_rect2.collidepoint(mouse_pos):
                print("Clic")
                salir()

background = pygame.image.load('welcomeInterfaceFramesSprites/SavedItems/bg.png').convert()  # Cargar la imagen de fondo
background = pygame.transform.scale(background, (screen_width, screen_height))  

# Agregar un label con el texto "battle city"
label = tk.Label(window, text="battle city", font=("Arial", 36), fg="white", bg="black")
label.place(relx=0.5, rely=0.5, anchor="center")

while True:
    for e in event.get():
        if e.type == QUIT: 
            pygame.quit()
            sys.exit()

    frame = int(time.time()*4)
    frame %= len(images)
    frame %= len(close)
    screen.blit(background, (0, 0))
    screen.blit(images[frame], (980,10))
    screen.blit(close[frame],(20,10))


    titleImage1()

    button1_rect = images[frame].get_rect(topleft=(980,10))
    button2_rect = close[frame].get_rect(topleft=(20,10))

    display.flip()

    check_click(button1_rect, button2_rect)

window.mainloop()
