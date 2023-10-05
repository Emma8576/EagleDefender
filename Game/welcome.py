import tkinter as tk
from tkinter import *
import pygame
from PIL import ImageTk, Image
import subprocess

window = tk.Tk()  
window.attributes("-fullscreen", True)  

def esc(event): 
    window.destroy()
window.bind('<Escape>', esc)
window.configure(cursor="star") 

fondo = tk.PhotoImage(file="welcomeInterfaceFramesSprites/SavedItems/bg.png") 
w, h = fondo.width(), fondo.height() 
window.geometry("%dx%d+0+0" % (w, h))
background_label = tk.Label(window, image=fondo) 
background_label.place(x=0, y=0, relwidth=1, relheight=1) 

pygame.init()

def leer_volumen():
    with open('volumen.txt', 'r') as archivo:
        return float(archivo.read())
volumen = leer_volumen()

def guardar_volumen(volumen):
    with open('volumen.txt', 'w') as archivo:
        archivo.write(str(volumen))

def cambiar_volumen():
    global volumen 
    if 'Up' in window.teclas_pulsadas:
        if volumen < 1.0:
            volumen += 0.01
            pygame.mixer.music.set_volume(volumen)
    elif 'Down' in window.teclas_pulsadas:
        if volumen > 0.0:
            volumen -= 0.01
            pygame.mixer.music.set_volume(volumen)
    window.after(10, cambiar_volumen)
    guardar_volumen(volumen)


def tecla_pulsada(evento):
    window.teclas_pulsadas.add(evento.keysym)

def tecla_soltada(evento):
    window.teclas_pulsadas.remove(evento.keysym)

def iniciar():
    pygame.mixer.music.load('welcomeInterfaceFramesSprites/Sounds/mainSound1.mp3')
    pygame.mixer.music.set_volume(volumen) 
    pygame.mixer.music.play() 

    window.teclas_pulsadas = set()
    window.bind('<KeyPress>', tecla_pulsada)
    window.bind('<KeyRelease>', tecla_soltada)
    window.after(10, cambiar_volumen)

iniciar() 

def salir(): 
    window.destroy()

def abrir():
    pygame.quit()  # Cierra la ventana de Pygame
    subprocess.call(["python", "Login.py"])

boton_cerrar=tk.Button(window, text="Abandonar la pista", 
                 command=salir, 
                 fg="gray1",
                 bg="DodgerBlue4",
                 relief="sunken",
             font=("System 18 bold"),
                 cursor="exchange")
boton_cerrar.pack()     
boton_cerrar.place(x=10,y=10, height=40, width=289) 


boton_abrir=tk.Button(window, text="Iniciar",
                    command=abrir,
                    fg="gray1",
                    bg="DodgerBlue4",
                    relief="sunken",
                    font=("System 18 bold"),
                    cursor="exchange")
boton_abrir.pack()     
boton_abrir.place(x=100,y=100, height=40, width=289) 



window.mainloop()
