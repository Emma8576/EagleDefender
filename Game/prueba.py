import tkinter as tk
from tkinter import filedialog
import os
import pymysql
import pygame
from pygame import mixer

ubicacion_temporal = os.path.expanduser("~")

# Inicializar pygame y mixer
pygame.init()
mixer.init()

cancion_actual = None
reproductor = None

# Función para guardar una canción en la base de datos
def guardar_cancion_en_db(nombre_cancion, file_path):
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="bd1",
        charset="utf8",
        connect_timeout=60
    )

    try:
        with conexion.cursor() as cursor:
            with open(file_path, 'rb') as archivo:
                contenido = archivo.read()
            consulta = "INSERT INTO canciones (nombre_cancion, archivo_cancion) VALUES (%s, %s)"
            cursor.execute(consulta, (nombre_cancion, contenido))
            conexion.commit()
    finally:
        conexion.close()

# Función para seleccionar un archivo de música y guardarlo en la base de datos
def seleccionar_y_guardar_musica():
    file_path = filedialog.askopenfilename(title="Seleccione una canción",
                                           filetypes=[("Audio files", "*.mp3 *.wav *.ogg")])
    if file_path:
        nombre_cancion = os.path.basename(file_path)  # Obtener el nombre del archivo
        guardar_cancion_en_db(nombre_cancion, file_path)
        print(f"Canción '{nombre_cancion}' guardada en la base de datos.")

# Función para cargar nombres de canciones desde la base de datos
def cargar_nombres_canciones():
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="bd1",
        charset="utf8",
        connect_timeout=60
    )

    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT nombre_cancion FROM canciones"
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            nombres = [resultado[0] for resultado in resultados]
            return nombres
    finally:
        conexion.close()

# Función para manejar la selección de una canción desde el Listbox
def seleccionar_cancion(event):
    global cancion_actual, reproductor

    if cancion_actual is not None and reproductor is not None and reproductor.get_busy():
        reproductor.stop()
        cancion_actual = None

    seleccion = lista_canciones.get(lista_canciones.curselection())
    print(f"Canción seleccionada: {seleccion}")

    # Conectar a la base de datos y obtener el archivo de la canción
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="bd1",
        charset="utf8",
        connect_timeout=60
    )

    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT archivo_cancion FROM canciones WHERE nombre_cancion = %s"
            cursor.execute(consulta, (seleccion,))
            resultado = cursor.fetchone()
            if resultado:
                # Guardar el archivo BLOB en un archivo temporal
                with open("musica_temp/temp_cancion.mp3", "wb") as archivo_temporal:
                    archivo_temporal.write(resultado[0])
                # Reproducir la canción desde el archivo temporal
                reproductor = mixer.music
                reproductor.load("musica_temp/temp_cancion.mp3")
                reproductor.play()
                cancion_actual = seleccion
            else:
                print("La canción no se encontró en la base de datos.")
    finally:
        conexion.close()

# Función para detener la reproducción
def detener_reproduccion():
    global cancion_actual, reproductor

    if cancion_actual is not None and reproductor is not None and reproductor.get_busy():
        reproductor.stop()
        cancion_actual = None

# Crear una ventana tkinter
ventana = tk.Tk()
ventana.title("Seleccionar y Reproducir Canción")

# Ajustar el tamaño de la ventana
ventana.geometry("800x400") 

# Crear un botón para seleccionar y guardar la canción
boton_seleccionar = tk.Button(ventana, text="Seleccionar y Guardar Canción", command=seleccionar_y_guardar_musica)
boton_seleccionar.pack(padx=20, pady=10)

# Crear un Listbox para mostrar los nombres de las canciones
nombres_canciones = cargar_nombres_canciones()
lista_canciones = tk.Listbox(ventana, height=10, width=100) 
for nombre in nombres_canciones:
    lista_canciones.insert(tk.END, nombre)
lista_canciones.pack(padx=20, pady=10)

# Asociar la función de selección a la lista
lista_canciones.bind('<<ListboxSelect>>', seleccionar_cancion)

# Botón para detener la reproducción
boton_detener = tk.Button(ventana, text="Detener Reproducción", command=detener_reproduccion)
boton_detener.pack(padx=20, pady=10)

# Iniciar el bucle principal de Tkinter
ventana.mainloop()
