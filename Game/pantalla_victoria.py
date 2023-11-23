import tkinter as tk
from tkinter import *
import subprocess
import time
import sys

# hacer variables de fuentes globales
global fuente_retro
global fuente_retro_1
global fuente_retro_2
global fuente_retro_3
global fuente_retro_4
global fuente_retro_5

# Se añade la fuente retro en diversos tamaños
fuente_retro = ("8-Bit Operator+ 8", 100)
fuente_retro_1 = ("8-Bit Operator+ 8", 40)
fuente_retro_2 = ("8-Bit Operator+ 8", 50)
fuente_retro_3 = ("8-Bit Operator+ 8", 25)
fuente_retro_4 = ("8-Bit Operator+ 8", 20)
fuente_retro_5 = ("8-Bit Operator+ 8", 15)

def volver_inicio_sesion():
    archivo = 'Login.py'
    try:
        subprocess.Popen(['python', archivo])
        time.sleep(1.5)
        sys.exit()
    except FileNotFoundError:
        print(f'El archivo "{archivo}" no se encontró o no se pudo ejecutar.')
        
# Función para cargar los nombres de usuario que iniciaron sesión
def cargar_nombres_usuarios():
    with open('nombres_usuarios.txt', 'r') as file:
        lineas = file.readlines()
        usuario_1 = lineas[0].strip().split(": ")[1]
        usuario_2 = lineas[1].strip().split(": ")[1]
        print(usuario_1)
        print(usuario_2)
        return usuario_1, usuario_2
        

def pantalla_victoria(ganador):
    ventana_victoria = tk.Tk()  # Crear una nueva instancia de Tk
    ventana_victoria.title("¡Victoria!")

    # Configurar la ventana para ocupar toda la pantalla
    ancho_pantalla = ventana_victoria.winfo_screenwidth()
    alto_pantalla = ventana_victoria.winfo_screenheight()
    ventana_victoria.attributes('-fullscreen', True)  # Pantalla completa
    ventana_victoria.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")

    # Cargar la imagen de fondo
    ruta_imagen = "loginImages/fondo1.png"
    imagen_fondo = tk.PhotoImage(file=ruta_imagen)
    label_fondo = tk.Label(ventana_victoria, image=imagen_fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Mantener una referencia a la imagen de fondo
    ventana_victoria.image_fondo = imagen_fondo

    # Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_victoria, text="Battle City",
                           bg="#000030",
                           font=fuente_retro,
                           fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.07, anchor='center')

    # Contenido de la pantalla de victoria
    etiqueta_victoria = tk.Label(ventana_victoria,
                                 text=f"¡Felicidades {ganador}!\n \n Has ganado.",
                                 font=fuente_retro_2,
                                 bg="#000030",
                                 fg="white",)
    
    etiqueta_victoria.place(relx=0.25, rely=0.4)
    
    
        # Botón de Salir
    global boton_salir
    boton_salir = tk.Button(ventana_victoria,
                            cursor="exchange",
                            text="Salir",
                            height="4",
                            width="30",
                            background="#0a0c3f",
                            fg="white",
                            font=fuente_retro_5,
                            relief="raised",
                            borderwidth=10,
                            command=volver_inicio_sesion)
    boton_salir.place(relx=0.5, rely=0.5 + 0.3, anchor='center')

    ventana_victoria.mainloop()

