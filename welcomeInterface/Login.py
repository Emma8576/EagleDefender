import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pymysql

# Variables globales para las ventanas
ventana1 = None
ventana2 = None

def menu_login():
    global ventana1
    # Crear una instancia de la ventana principal
    ventana1 = tk.Tk()
    ventana1.attributes("-fullscreen", True)
    
    # Establecer el título de la ventana
    ventana1.title("Bienvenidos")

    # Cargar icono de la ventana
    ventana1.iconbitmap("images/icon.ico")

    image = PhotoImage(file="images/logoLogin.png")
    image = image.subsample(1, 1)
    label = Label(image=image)
    label.pack()
    
    # Agregar una etiqueta de texto en el inicio de sesión
    etiqueta = Label(ventana1, text="Acceder al juego", bg="peru", fg="white", width="800", height="2", font=("calibri", 40))
    etiqueta.pack()

    # Botón de iniciar sesión
    botonInicio = tk.Button(text="Iniciar Sesión", command=inicio_sesion, height="3", width="30")
    botonInicio.place(x=575, y=400)

    # Botón de Registrarse
    botonInicio = tk.Button(text="Registrarse", height="3", width="30")
    botonInicio.place(x=575, y=475)
    
    # Botón de salir del juego
    botonInicio = tk.Button(text="Salir", height="3", width="30", command=cerrarJuego)
    botonInicio.place(x=575, y=550)
    # Mostrar la ventana principal
    ventana1.mainloop()

#Funcion para cerrar el juego
def cerrarJuego():
    ventana1.destroy()
    
# Función para mostrar la ventana de inicio de sesión
def inicio_sesion():
    global ventana2
    if ventana1:
        ventana1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana2 = Toplevel(ventana1)
    ventana2.attributes("-fullscreen", True)
    ventana2.title("Iniciar sesión")

    # Agregar la pantalla de inicio de sesión en la misma ventana
    etiqueta = Label(ventana2, text="Por favor ingrese su Usuario y Contraseña", bg="peru", fg="white", width="800", height="2", font=("calibri", 30))
    etiqueta.pack()

    nombreUsuario_verif = StringVar() 
    contrasenaUsuario_verif = StringVar()

    Label(ventana2, text="Usuario").pack()
    nombre_usuario_entry = Entry(ventana2, textvariable=nombreUsuario_verif)
    nombre_usuario_entry.pack()
    Label(ventana2).pack()

    Label(ventana2, text="Contraseña").pack()
    contrasena_usuario_entry = Entry(ventana2, textvariable=contrasenaUsuario_verif)
    contrasena_usuario_entry.pack()
    Label(ventana2).pack()

    # Botón de Atrás de la ventana inicio de sesión
    botonAtras = Button(ventana2, text="Atrás", width=30, height=3, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.5)

    ventana2.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana
    
    ventana2.mainloop()

# Función para volver atrás
def volver_atras():
    global ventana2
    if ventana2:
        ventana2.withdraw()
    if ventana1:
        ventana1.deiconify()

menu_login()
