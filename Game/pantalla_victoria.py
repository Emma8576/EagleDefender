import tkinter as tk
from tkinter import *
import subprocess
import time
import sys
import pymysql
import random
import pygame
import tempfile
import os
import win32gui
import win32con
import psutil

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
        os.execl(sys.executable, sys.executable, archivo)
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
        
###########################Funciones para obtener la música de cada jugador###########################
# Función para reproducir la música desde un archivo temporal
def reproducir_musica_desde_temp(cancion_temp):
    pygame.mixer.init()
    pygame.mixer.music.load(cancion_temp)
    pygame.mixer.music.play()

# Función para obtener los nombres de usuario de los roles
def obtener_nombres_roles():
    try:
        with open('nombres_usuarios.txt', 'r') as file:
            lineas = file.readlines()
            usuario_defensor = lineas[0].strip().split(": ")[1]
            usuario_atacante = lineas[1].strip().split(": ")[1]
            return usuario_defensor, usuario_atacante
    except FileNotFoundError:
        print("El archivo nombres_usuarios.txt no fue encontrado.")

# Ejemplo de uso
nombre_defensor, nombre_atacante = obtener_nombres_roles()
print(f"El defensor es: {nombre_defensor}")
print(f"El atacante es: {nombre_atacante}")

def obtener_canciones_atacante(nombre_usuario_atacante):
    canciones_atacante = []
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="bd1",
            charset="utf8",
            connect_timeout=60
        )

        with conexion.cursor() as cursor:
            # Consulta SQL para obtener el ID del usuario atacante por su nombre
            sql_usuario = "SELECT ID FROM login WHERE Usuario = %s"
            cursor.execute(sql_usuario, (nombre_usuario_atacante,))
            id_usuario_atacante = cursor.fetchone()

            if id_usuario_atacante:
                # Consulta SQL para obtener las canciones asociadas al ID del usuario atacante
                sql_canciones = """
                    SELECT c.nombre_cancion 
                    FROM usuarios_canciones uc
                    JOIN canciones c ON uc.id_cancion = c.ID
                    WHERE uc.id_usuario = %s
                """
                cursor.execute(sql_canciones, (id_usuario_atacante[0],))
                result = cursor.fetchall()

                if result:
                    canciones_atacante = [cancion[0] for cancion in result]

                    # Escoge una canción aleatoria
                    cancion_aleatoria = random.choice(canciones_atacante)

                    # Descarga la canción desde la base de datos
                    cursor.execute("SELECT archivo_cancion FROM canciones WHERE nombre_cancion = %s", (cancion_aleatoria,))
                    cancion_blob = cursor.fetchone()[0]

                    # Guarda la canción en un archivo temporal
                    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                    temp_file.write(cancion_blob)
                    temp_file.close()

                    # Reproduce la canción desde el archivo temporal
                    reproducir_musica_desde_temp(temp_file.name)
                    print(f"Reproduciendo la canción: {cancion_aleatoria}")

    except pymysql.Error as e:
        print(f"Error al obtener las canciones asociadas al usuario atacante por nombre: {str(e)}")
    finally:
        if conexion:
            conexion.close()

    return canciones_atacante


#Defensor
# Función para reproducir la música desde un archivo temporal
def reproducir_musica_desde_temp2(cancion_temp2):
    pygame.mixer.init()
    pygame.mixer.music.load(cancion_temp2)
    pygame.mixer.music.play()
    
def obtener_canciones_defensor(nombre_usuario_defensor):
    canciones_defensor = []
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="bd1",
            charset="utf8",
            connect_timeout=60
        )

        with conexion.cursor() as cursor:
            # Consulta SQL para obtener el ID del usuario defensor por su nombre
            sql_usuario = "SELECT ID FROM login WHERE Usuario = %s"
            cursor.execute(sql_usuario, (nombre_usuario_defensor,))
            id_usuario_defensor = cursor.fetchone()

            if id_usuario_defensor:
                # Consulta SQL para obtener las canciones asociadas al ID del usuario defensor
                sql_canciones = """
                    SELECT c.nombre_cancion 
                    FROM usuarios_canciones uc
                    JOIN canciones c ON uc.id_cancion = c.ID
                    WHERE uc.id_usuario = %s
                """
                cursor.execute(sql_canciones, (id_usuario_defensor[0],))
                result = cursor.fetchall()

                if result:
                    canciones_defensor = [cancion[0] for cancion in result]

                    # Escoge una canción aleatoria
                    cancion_aleatoria = random.choice(canciones_defensor)

                    # Descarga la canción desde la base de datos
                    cursor.execute("SELECT archivo_cancion FROM canciones WHERE nombre_cancion = %s", (cancion_aleatoria,))
                    cancion_blob = cursor.fetchone()[0]

                    # Guarda la canción en un archivo temporal
                    temp_file2 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                    temp_file2.write(cancion_blob)
                    temp_file2.close()

                    # Reproduce la canción desde el archivo temporal
                    reproducir_musica_desde_temp2(temp_file2.name)
                    print(f"Reproduciendo la canción: {cancion_aleatoria}")

    except pymysql.Error as e:
        print(f"Error al obtener las canciones asociadas al usuario defensor por nombre: {str(e)}")
    finally:
        if conexion:
            conexion.close()

    return canciones_defensor



###########################Fin de funciones para obtener la música de cada jugador####################

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

#pantalla_victoria("memo")