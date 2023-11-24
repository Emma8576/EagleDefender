"""Código mantenido por Bryan Monge - 2023026192"""

import pygame
import sys
import pygame.time
from pygame import *
from pygame import time as pygame_time
import subprocess
import os
import datetime
import json
import io
import random
import pymysql.cursors
import threading
import mutagen.mp3
import time
from pantalla_victoria import pantalla_victoria

# Colores de bloques
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)

pygame.init()
# Obtener información de pantalla y ajustar a pantalla completa
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)
# Ruta al archivo .ttf de la fuente y tamaño
ruta_fuente = "Fuentes/8bitOperatorPlus8-Bold.ttf"
tamaño_fuente_texto = 50
tamaño_fuente_titulo = 90
tiempo_restante = 0
tiempo_restante2 = 0
mostrar_mensaje = False
tiempo_mensaje = 0
duracion_mensaje = 1000
# Cargar la fuente texto
fuente_pausa_1 = pygame.font.Font(ruta_fuente, tamaño_fuente_texto)
# Cargar la fuente titulo
fuente_pausa_2 = pygame.font.Font(ruta_fuente, tamaño_fuente_titulo)

#Se cargan los sonidos que se ejecutan según el tipo de munición disparada
pygame.mixer.init()
agua = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/agua.wav")
fuego = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/fuego.wav")
bomba = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/bomba.wav")

#Se cargan los sonidos que se ejecutan según el tipo de bloque puesto
madera = pygame.mixer.Sound("panel_elements\\defensor_elementos\\bloques_sonido\\madera.mp3")
concreto = pygame.mixer.Sound("panel_elements\\defensor_elementos\\bloques_sonido\\concreto.mp3")
acero = pygame.mixer.Sound("panel_elements\\defensor_elementos\\bloques_sonido\\acero.mp3")

# Cargar background
bg = pygame.image.load("panel_elements/bg/bag.jpg")

# Función para dibujar el mensaje de fin de tiempo en la pantalla
def mostrar_mensaje_fin_tiempo(screen):
    global mostrar_mensaje, tiempo_inicio_mensaje, tiempo_restante  # Declarar como variables globales para modificarlas dentro de la función
    font = pygame.font.Font(None, 78)
    text = font.render(" ", True, (255, 0, 0))  # Mensaje en rojo
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centrar el mensaje en la pantalla

    if tiempo_restante <= 0:
        if not mostrar_mensaje:  # Mostrar el mensaje solo una vez al llegar a cero el tiempo
            mostrar_mensaje = True
            tiempo_inicio_mensaje = pygame.time.get_ticks()  # Guardar el tiempo actual

    if mostrar_mensaje:
        tiempo_actual = pygame.time.get_ticks()
        screen.blit(text, text_rect)  # Mostrar el mensaje

        if tiempo_actual - tiempo_inicio_mensaje >= 1000:  # Ocultar el mensaje después de 1 segundo (1000 milisegundos)
            mostrar_mensaje = False  # Desactivar la bandera para ocultar el mensaje


def mostrar_temporizador(screen):
    if tiempo_restante > 0:
        font = pygame.font.Font(None, 36)  # Fuente y tamaño del texto
        text = font.render(f'Tiempo restante: {tiempo_restante // 60:02}:{tiempo_restante % 60:02}', True, (255, 255, 255))  # Renderizar el texto
        screen.blit(text, (10, 10))

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, posicion, tamano=30, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, tamano)
    texto_renderizado = font.render(texto, True, color)
    screen.blit(texto_renderizado, posicion)

def obtener_duracion_cancion(archivo):
    audio = mutagen.mp3.MP3(archivo)
    return int(audio.info.length)


def reproducir_musica():
    try:
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="bd1",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        # Inicializar Pygame y mezclar las canciones para reproducir una aleatoria
        pygame.init()
        pygame.mixer.init()

        # Obtener los archivos de canciones de la base de datos
        cursor = conexion.cursor()
        cursor.execute("SELECT archivo_cancion FROM canciones")
        canciones = cursor.fetchall()
        archivos_canciones = [io.BytesIO(cancion['archivo_cancion']) for cancion in canciones]

        # Mezclar las canciones para reproducir una aleatoria
        cancion_aleatoria = random.choice(archivos_canciones)

        # Guardar el archivo de canción temporalmente en el sistema de archivos local
        with open('musica_temp/temp_song.mp3', 'wb') as temp_file:
            temp_file.write(cancion_aleatoria.read())

        # Cargar la canción desde el archivo temporal con Pygame
        pygame.mixer.music.load('musica_temp/temp_song.mp3')

        # Reproducir la canción de fondo en bucle
        pygame.mixer.music.play(-1)

        # Mantener la reproducción hasta que se indique lo contrario
        while not stop_music_event.is_set():
            time.sleep(1)  # Utiliza la función sleep del módulo time

    except Exception as e:
        print("Error:", e)
    finally:
        # Cerrar la conexión y detener la música al finalizar
        if 'conexion' in locals():
            conexion.close()
        pygame.mixer.music.stop()


# Crear un evento para controlar la reproducción de la música
stop_music_event = threading.Event()

# Iniciar la reproducción de música en un hilo separado
thread_musica = threading.Thread(target=reproducir_musica)
thread_musica.start()

time.sleep(1)
# Ruta del archivo de música
archivo_musica = 'musica_temp/temp_song.mp3'

# Obtener la duración de la canción
duracion = obtener_duracion_cancion(archivo_musica)

# Convertir la duración a minutos y segundos
minutos = duracion // 60
segundos = duracion % 60

tiempo_restante = duracion

# Imprimir la duración en la terminal
print(f'Duración de la canción: {minutos} minutos y {segundos} segundos')


# Mostrar cuenta regresiva en la terminal en tiempo real
def cuenta_regresiva():
    global tiempo_restante
    while tiempo_restante > 0:
        pygame.display.flip()
        minutos = tiempo_restante // 60
        segundos = tiempo_restante % 60
        sys.stdout.write(f'\rTiempo restante: {minutos:02}:{segundos:02}')  # Actualizar la misma línea en la terminal
        sys.stdout.flush()
        time.sleep(1)  # Esperar 1 segundo
        tiempo_restante -= 1

    print("\n¡La canción ha terminado!")

    stop_music_event.set()

    # Reproducir una nueva canción aleatoria

# Iniciar el hilo para la cuenta regresiva
thread_cuenta_regresiva = threading.Thread(target=cuenta_regresiva)
thread_cuenta_regresiva.start()

def mostrar_temporizador2(screen):
    font = pygame.font.Font(None, 36)  # Fuente y tamaño del texto
    text2 = font.render(f'Tiempo restante: {tiempo_restante2 // 60:02}:{tiempo_restante2 % 60:02}', True, (255, 255, 255))  # Renderizar el texto
    screen.blit(text2, (10, 10))
    
def reproducir_nueva_cancion():
    try:
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="bd1",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        # Obtener los archivos de canciones de la base de datos
        cursor = conexion.cursor()
        cursor.execute("SELECT archivo_cancion FROM canciones")
        canciones = cursor.fetchall()
        archivos_canciones = [io.BytesIO(cancion['archivo_cancion']) for cancion in canciones]

        # Mezclar las canciones para reproducir una aleatoria
        cancion_aleatoria = random.choice(archivos_canciones)

        # Guardar el archivo de canción temporalmente en el sistema de archivos local
        with open('musica_temp/temp_cancion.mp3', 'wb') as temp_file:
            temp_file.write(cancion_aleatoria.read())

        # Cargar la nueva canción desde el archivo temporal con Pygame
        pygame.mixer.music.load('musica_temp/temp_cancion.mp3')

        # Reproducir la nueva canción de fondo en bucle
        pygame.mixer.music.play(-1)

        # Restablecer el evento para la reproducción de música
        stop_music_event.clear()

        # Reiniciar el temporizador


    except Exception as e:
        print("Error:", e)
    finally:
        # Cerrar la conexión al finalizar
        if 'conexion' in locals():
            conexion.close()

archivo_musica2 = 'musica_temp/temp_cancion.mp3'

duracion2 = obtener_duracion_cancion('musica_temp/temp_cancion.mp3')

minutos2 = duracion2 // 60
segundos2 = duracion2 % 60

def cuenta_regresiva2():
    global tiempo_restante2
    tiempo_restante2 = duracion2
    while tiempo_restante2 > 0:
        pygame.display.flip()
        minutos2 = tiempo_restante2 // 60
        segundos2 = tiempo_restante2 % 60
        sys.stdout.write(f'\rTiempo restante: {minutos2:02}:{segundos2:02}')  # Actualizar la misma línea en la terminal
        sys.stdout.flush()
        time.sleep(1)  # Esperar 1 segundo
        tiempo_restante2 -= 1

    print("\n¡La canción ha terminado!")

    stop_music_event.set()


thread_cuenta_regresiva2 = threading.Thread(target=cuenta_regresiva2)
thread_cuenta_regresiva2.start()

if tiempo_restante2 == 0:
    pygame.mixer.music.stop()

def escalar_imagenes(imagenes, factor):
    """
    Función que escala imagenes según el factor de proporción dado para los frames de los personakes para el ajuste de pantalla según el tamaño

    *pygame.transform.scale(imagen, (int(imagen.get_width()*factor), int(imagen.get_height()*factor))):
        Escala la imagen tomando como argumentos la imagen que se va a escalar y la tupla que especifica el nuevo tamaño
    **for imagen in lista
        Itera sobre cada imagen en la lista correspondiente
    **for direccion, lista in imagenes.items()
        Itera sobre el diccionario, donde se toma como parámetro la direccion (ej: "up") y la lista, que corresponde a la direccion
     """
    return {direccion: [pygame.transform.scale(imagen, (int(imagen.get_width()*factor), int(imagen.get_height()*factor))) for imagen in lista] for direccion, lista in imagenes.items()}

#/////////////Contenido pantalla de pausa//////////////////////

# Función que muestra un mensaje en la pantalla de juego.

def salir():
    pygame.mixer.music.stop()
    pygame.quit()
    subprocess.run(["python", "Login.py"])
    sys.exit()
 

 #/////////////Contenido pantalla de pausa//////////////////////

def message_screen(message, font, color, y_displacement=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2 + y_displacement)
    screen.blit(text, text_rect)


def ventana_ayuda():
    white = (255,255,255)

    fondo = pygame.image.load("loginImages/fondo_reducido.png")

    ventana_mensaje_aparece = True
    while ventana_mensaje_aparece:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ventana_mensaje_aparece = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    ventana_mensaje_aparece = False


            screen.blit(fondo, (0,0))

            message_screen("Aquí va todo lo de como jugar", fuente_pausa_1, white, 25)
            pygame.display.update()
            clock.tick(5)
          
    # función de pausa
def pause():
    white = (255, 255, 255)
    
    # Cargar la imagen de fondo
    fondo = pygame.image.load("loginImages/fondo_reducido.png")

    
    
    #Función de pausar el juego
    pausa = True
    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pausa = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pausa = False
                elif event.key == pygame.K_q:
                    pausa = False
                    salir()

                               
            screen.blit(fondo, (0,0))
            
            message_screen("Battle City",
                    fuente_pausa_2,
                    white,
                    -300)
            
            message_screen("Juego pausado",
                        fuente_pausa_1,
                        white,
                        -100)
            message_screen("Presiona C para continuar o Q para salir",
                        fuente_pausa_1,
                        white,
                        25)

            message_screen("Presiona X para obtener ayuda sobre cómo jugar",
                        fuente_pausa_1,
                        white,
                        100)
            pygame.display.update()
            clock.tick(5)


            
def leer_roles(archivo):
    roles = {}
    with open(archivo, 'r') as file:
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                key, value = parts
                roles[key] = value
    return roles

roles = leer_roles('nombres_usuarios.txt')

# Obtener los nombres de usuario para el Atacante y el Defensor
atacante_name = roles.get('Atacante', 'Atacante no identificado')
defensor_name = roles.get('Defensor', 'Defensor no identificado')

# Imprimir los nombres de usuario
print('\nNombre del Atacante:', atacante_name)
print('Nombre del Defensor:', defensor_name)
              
#/////////////////////Fin pantalla de pausa////////////////////////
             
# Clase base para los personajes
class Personaje:
    """Author:Bryan Monge
    
    Class: Diccionario con imágenes del personaje para diferentes direcciones 

           image_paths: diccionario que contiene las rutas de los archivos de las imágenes en las diferentes direcciones
           start_pos: indica la posición inicial del personaje

    """
    def __init__(self, image_paths, start_pos):
        self.images = escalar_imagenes({
            "up": [pygame.image.load(image_path) for image_path in image_paths["up"]],
            "down": [pygame.image.load(image_path) for image_path in image_paths["down"]],
            "right": [pygame.image.load(image_path) for image_path in image_paths["right"]],
            "left": [pygame.image.load(image_path) for image_path in image_paths["left"]],
            "ul": [pygame.image.load(image_path) for image_path in image_paths["ul"]],
            "ur": [pygame.image.load(image_path) for image_path in image_paths["ur"]],
            "dl": [pygame.image.load(image_path) for image_path in image_paths["dl"]],
            "dr": [pygame.image.load(image_path) for image_path in image_paths["dr"]],
        },0.7)

        self.current_frame = 0
        self.rect = self.images["up"][0].get_rect() #Rectángulo para detectar posicionamiento y colisiones
        self.rect.topleft = start_pos
        self.direction = "up"
    def mover(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        # Restringir el movimiento para mantener al personaje dentro de la pantalla
        if screen.get_rect().contains(new_rect):
            # Limitar el movimiento hacia arriba
            if new_rect.top >= 100:
                self.rect = new_rect


    #Dibuja al personaje en la direccion actual
    def dibujar(self):
        if self.images:
            screen.blit(self.images[self.direction][self.current_frame], self.rect)
    #Cambiar la direccion del personaje
    def cambiar_direccion(self, new_direction):
        self.direction = new_direction
    #Actualizar el cuadro de animación del personaje
    def actualizar_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])

# Clase que representa al personaje Atacante en el juego. Hereda de la clase Personajes
class Atacante(Personaje):
    """Author: Bryan Monge"""
    def __init__(self, start_pos):
        image_paths = {
            "up": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_up/frame-{i}.gif" for i in range(1, 5)],
            "down": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_down/frame-{i}.gif" for i in range(1, 5)],
            "right": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_right/frame-{i}.gif" for i in range(1, 5)],
            "left": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_left/frame-{i}.gif" for i in range(1, 5)],
            "ul": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_ul/frame-{i}.png" for i in range(1, 5)],
            "ur": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_ur/frame-{i}.png" for i in range(1, 5)],
            "dl": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_dl/frame-{i}.png" for i in range(1, 5)],
            "dr": [f"panel_elements/atacante_elementos/atacante_direccion/atacante_dr/frame-{i}.png" for i in range(1, 5)],
        }
        super().__init__(image_paths, start_pos)
#agua, fuego, bomba
#acero, concreto y madera
         #1 bomba, una bola fuego, 2 bola de agua
         #1 bomba, dos bolas fuego, tres de agua
         #1 de cualquiera
        self.last_shot_time = 0 #tiempo del último disparo
        self.bullets = []

        self.municiones = {"fuego": proyectilFuego, "hielo": proyectilHielo, "bomba": proyectilBomba} #Diccionario que mapea los tipos de municiones a las clases
        self.current_municion = "fuego"

        self.agua = agua #Efecto de sonido agua
        self.fuego = fuego #Efecto de sonido fuego
        self.bomba = bomba #Efecto de sonido bomba

        self.municiones_restantes = {"fuego":5, "hielo":5, "bomba":5}
        self.last_shot_time = 0
        self.last_regeneration_time = {"fuego": datetime.datetime.now().timestamp(),"hielo": datetime.datetime.now().timestamp(),"bomba": datetime.datetime.now().timestamp()}
        #cambia el tipo de saldo
    def cambiar_tipo_munición(self, tipo):
        self.current_municion = tipo

    #Dispara un proyectil en la dirección actual
    def disparar(self):
        if self.municiones_restantes[self.current_municion] > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= 1000: #Intervalo de un segundo por disparo
                self.last_shot_time = current_time
                municion = self.municiones[self.current_municion]
                bullet = municion(self.rect.topleft, self.direction)
                self.bullets.append(bullet)

                self.municiones_restantes[self.current_municion] -= 1

                #Reproduce los sonidos por cada tipo de munición
                if self.current_municion == "agua":
                    self.agua.play()
                elif self.current_municion == "fuego":
                    self.fuego.play()
                elif self.current_municion == "bomba":
                    self.bomba.play()
                    
    def obtener_posicion_A(self):
        return self.rect.center

    def regenerar_municiones(self):
        current_time = datetime.datetime.now().timestamp()
        if current_time - self.last_regeneration_time.get(self.current_municion, 0) >= 30:
            self.last_regeneration_time[self.current_municion] = current_time
            self.municiones_restantes[self.current_municion] = min(self.municiones_restantes[self.current_municion] +1,5)

    def dibujar(self):#
        if tiempo_restante == 0 and self.images:
            screen.blit(self.images[self.direction][self.current_frame], self.rect)

municion_restante = {
    "hielo": 5,
    "fuego": 5,
    "bomba": 5
}
#Clase que representa el tipo de municion Fuego
class proyectilFuego:
    """Author: Bryan Monge
       start_pos: indica la posicíón inicial del proyectl
       direction: dirección inicial del proyectil

    """
    def __init__(self, start_pos, direction):
        self.images = escalar_imagenes ({ #diccionario que contiene las direcciones del proyectil
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_up/frame-1.gif")],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_down/frame-1.gif")],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_left/frame-1.gif")],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_right/frame-1.gif")],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-2.gif") ],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-2.gif") ],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-2.gif")],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-2.gif")],
        }, 0.5)


        self.direction = direction #Dirección del proyectil
        self.current_frame = 0    
        self.image = self.images[direction][0] #Imagen actual del proyectil
        self.rect = self.image.get_rect() #Representa la posición y tamaño del proyectil
        self.rect.topleft = start_pos

        self.start_time = pygame.time.get_ticks()
        
        self.distancia_recorrida = 0      #Mueve el proyectil en la clase especificada
    #Si la dirección actual es __ entonces se mueve "x" y "y" unidades
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0, -6)
        elif self.direction == "down":
            self.rect.move_ip(0, 6)
        elif self.direction == "left":
            self.rect.move_ip(-6, 0)
        elif self.direction == "right":
            self.rect.move_ip(6, 0)
        elif self.direction == "ul":
            self.rect.move_ip(-6, -6)
        elif self.direction == "ur":
            self.rect.move_ip(6, -6)
        elif self.direction == "dl":
            self.rect.move_ip(-6, 6)
        elif self.direction == "dr":
            self.rect.move_ip(6, 6)
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 2500:
            self.rect.topleft = (-100, -100)

        self.distancia_recorrida += abs(dx) + abs(dy)  # Actualiza la distancia recorrida
        

        for bloque in defensor.bloques:
            if self.rect.colliderect(bloque.rect):
                tipo_proyectil = self.__class__.__name__
                bloque.impacto(tipo_proyectil)
                self.rect.topleft = (-100, -100)

        current_images = self.images.get(self.direction, [])
        if current_images:
            self.image = current_images[0] 

        

    #Verifica si el proyectil está dentro de la pantalla, sino, este es destruido
    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)

class proyectilHielo:
    def __init__(self, start_pos, direction):
        self.images = escalar_imagenes({
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_up/{i}.png") for i in range(1,16)],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_down/{i}.png") for i in range(1,16)],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_left/{i}.png") for i in range(1,16)],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_right/{i}.png") for i in range(1,16)],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_ud/{i}.png") for i in range(1,16)],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_ud/{i}.png") for i in range(1,16)],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_ud/{i}.png") for i in range(1,16)],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/hielo/atacante_munición_ud/{i}.png") for i in range(1,16)],
        }, 0.9)
        self.rect = self.images[direction][0].get_rect()
        self.rect.topleft = start_pos
        self.direction = direction
        self.current_frame = 0
        self.image = self.images[direction][0]

        self.start_time = pygame.time.get_ticks()
        
        
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0,-5)
        elif self.direction == "down":
            self.rect.move_ip(0,5)
        elif self.direction == "left":
            self.rect.move_ip(-5,0)
        elif self.direction == "right":
            self.rect.move_ip(5,0)
        elif self.direction == "ul":
            self.rect.move_ip(-5,-5)
        elif self.direction == "ur":
            self.rect.move_ip(5,-5)
        elif self.direction == "dl":
            self.rect.move_ip(-5,5)
        elif self.direction == "dr":
            self.rect.move_ip(5,5)
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 2500:
            self.rect.topleft = (-100, -100)

        for bloque in defensor.bloques:
            if self.rect.colliderect(bloque.rect):
                tipo_proyectil = self.__class__.__name__
                bloque.impacto(tipo_proyectil)
                self.rect.topleft = (-100, -100)

    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)



class proyectilBomba:
    def __init__(self, start_pos, direction):
        self.images = escalar_imagenes({
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_up/frame-{i}.gif") for i in range(1,9)],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_down/frame-{i}.gif") for i in range(1,9)],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_left/frame-{i}.gif") for i in range(1,9)],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_right/frame-{i}.gif") for i in range(1,9)],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_ul/{i}.png") for i in range(1,9)],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_ur/{i}.png") for i in range(1,9)],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_dl/{i}.png") for i in range(1,9)],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion//bomba/atacante_municion_dr/{i}.png") for i in range(1,9)],
        },0.3)
        self.rect = self.images[direction][0].get_rect()
        self.rect.topleft = start_pos
        self.direction = direction
        self.current_frame = 0
        self.image = self.images[direction][0]

        self.start_time = pygame.time.get_ticks()
        
        
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0,-7)
        elif self.direction == "down":
            self.rect.move_ip(0,7)
        elif self.direction == "left":
            self.rect.move_ip(-7,0)
        elif self.direction == "right":
            self.rect.move_ip(7,0)
        elif self.direction == "ul":
            self.rect.move_ip(-7,-7)
        elif self.direction == "ur":
            self.rect.move_ip(7,-7)
        elif self.direction == "dl":
            self.rect.move_ip(-7,7)
        elif self.direction == "dr":
            self.rect.move_ip(7,7)
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= 2500:
            self.rect.topleft = (-100, -100)

        for bloque in defensor.bloques:
            if self.rect.colliderect(bloque.rect):
                tipo_proyectil = self.__class__.__name__
                bloque.impacto(tipo_proyectil)
                self.rect.topleft = (-100, -100)


    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)

    


# Clase que representa al personaje Defensor. Hereda de la clase Personake
def agregar_al_salon_de_fama(tiempo_transcurrido):
    pass


class Defensor(Personaje):
    def __init__(self, start_pos):
        image_paths = {
            "up": [f"panel_elements/defensor_sprites/defensor_up/frame-{i}.gif" for i in range(1, 25)],
            "down": [f"panel_elements/defensor_sprites/defensor_down/frame-{i}.gif" for i in range(1, 25)],
            "right": [f"panel_elements/defensor_sprites/defensor_right/frame-{i}.gif" for i in range(1, 25)],
            "left": [f"panel_elements/defensor_sprites/defensor_left/frame-{i}.gif" for i in range(1, 25)],
            "ul": [f"panel_elements/defensor_sprites/defensor_ul/{i}.png" for i in range(1, 25)],
            "ur": [f"panel_elements/defensor_sprites/defensor_ur/{i}.png" for i in range(1, 25)],
            "dl": [f"panel_elements/defensor_sprites/defensor_dl/{i}.png" for i in range(1, 25)],
            "dr": [f"panel_elements/defensor_sprites/defensor_dr/{i}.png" for i in range(1, 25)],
        }
        super().__init__(image_paths, start_pos)

        self.images = escalar_imagenes(self.images, 0.8)

        self.vida = 1  # Agrega una variable de vida inicial

        self.bloque_seleccionado = "madera"  

        self.tiempo_destruccion = None

        self.bloques = []

        self.bloque_seleccionado = Bloque_madera

        self.bloques_maximos = {"madera": 10, "concreto": 10, "hierro": 10}

        self.bloques_colocados = {"madera": 0, "concreto": 0, "hierro": 0}



    def colocar_bloque(self):
        x, y = self.rect.center
        tipo_bloque = self.bloque_seleccionado.__name__.split("_")[1]
        
        if self.bloques_colocados[tipo_bloque] < self.bloques_maximos[tipo_bloque]:
            bloque = self.bloque_seleccionado(x, y)
            self.bloques.append(bloque)
            self.bloques_colocados[tipo_bloque] += 1

    def alcanzado_limite_bloques(self):
        tipo_bloque = self.bloque_seleccionado.__name__.split("_")[1]
        return self.bloques_colocados[tipo_bloque] >= self.bloques_maximos[tipo_bloque]


    def cambiar_tipo_bloque(self, tipo_bloque):
        if tipo_bloque == "p":
            self.bloque_seleccionado = Bloque_madera
        elif tipo_bloque == "o":
            self.bloque_seleccionado = Bloque_concreto
        elif tipo_bloque == "u":
            self.bloque_seleccionado = Bloque_hierro

    def impacto(self, tipo_proyectil):
        if tipo_proyectil == "fuego" or tipo_proyectil == "hielo" or tipo_proyectil == "bomba":
            self.vida -= 1
            


        if self.vida <= 0 or self.vida == 0:
            self.desaparecer()
        



    def desaparecer(self):
        self.vida = 0
        tiempo_transcurrido =   pygame.time.get_ticks() / 1000 - (start_time/1000)
        self.agregar_al_salon_de_fama(tiempo_transcurrido)
        from pantalla_victoria import pantalla_victoria 
        from pantalla_victoria import obtener_canciones_atacante
        obtener_canciones_atacante(atacante_name)
        pantalla_victoria(atacante_name)
        time.sleep(3)
        os._exit(0)


    

    def agregar_al_salon_de_fama(self, tiempo_transcurrido):
        global screen
        with open("nombres_usuarios.txt", "r") as file:
            lineas = file.readlines()
            atacante = lineas[1].split(":")[1].strip()

        with open("salon_de_fama.txt", "a") as file:
            file.write(f"{atacante} - {tiempo_transcurrido:.3f}\n")


    def obtener_posicion_D(self):
        return self.rect.center

    def dibujar(self):#
        if self.vida > 0 and self.images:
            screen.blit(self.images[self.direction][self.current_frame], self.rect)

class Bloque_madera:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("panel_elements\\defensor_elementos\\bloques_animacion\\madera\\1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.vida = 3

    def impacto(self, tipo_proyectil):
        if tipo_proyectil == "bomba" or tipo_proyectil == "fuego" or tipo_proyectil == "hielo":
            self.vida -= 1

        if self.vida <= 0:
            self.rect.topleft = (-100,-100)


    def dibujar(self, screen):
        if self.vida > 0:
            screen.blit(self.image, self.rect)

class Bloque_hierro:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("panel_elements\\defensor_elementos\\bloques_animacion\\hierro\\1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.vida = 3

    def impacto(self, tipo_proyectil):
        print(f"Vida antes del impacto: {self.vida}")

        if tipo_proyectil == "bomba" or tipo_proyectil == "fuego":
            self.vida -=2
        elif tipo_proyectil == "hielo":
            self.vida -= 1

        if self.vida <= 0:
            self.desaparecer()

        print(f"Vida después del impacto: {self.vida}")
        

    def desaparecer(self):
        self.vida = 0



    def dibujar(self, screen):
        if self.vida > 0:
            screen.blit(self.image, self.rect)



class Bloque_concreto:
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("panel_elements\\defensor_elementos\\bloques_animacion\\concreto\\1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.vida = 3

    def impacto(self, tipo_proyectil):
        # Ajustar la reducción de vida para el tipo de proyectil "fuego"
        if tipo_proyectil == "bomba":
            self.vida -= 3
        elif tipo_proyectil == "fuego":
            self.vida -= 1.5
        elif tipo_proyectil == "hielo":
            self.vida -= 1

        if self.vida <= 0:
            self.rect.topleft = (-100, -100)

    def dibujar(self, screen):
        if self.vida > 0:
            screen.blit(self.image, self.rect)



#Clase para los bloques
WHITE = (255, 255, 255)

bloques_creados = {
    "madera": 0,
    "concreto": 0,
    "acero": 0
}
#
bloques_restantes = {
    "madera": 10,
    "concreto": 10,
    "acero": 10
}


# Diccionarios para contar cuántos bloques de cada tipo se han creado


# Cargar imágenes
imagen_madera = pygame.image.load("panel_elements\\defensor_elementos\\madera.png")
imagen_concreto = pygame.image.load("panel_elements\\defensor_elementos\\concreto.png")
imagen_acero = pygame.image.load("panel_elements\\defensor_elementos\\Iron.png") 

# Escalar imágenes (si es necesario)
imagen_madera = pygame.transform.scale(imagen_madera, (50, 50))
imagen_concreto = pygame.transform.scale(imagen_concreto, (50, 50))
imagen_acero = pygame.transform.scale(imagen_acero, (50, 50))

# Diccionario para mapear tipo de bloque a su imagen y resistencia
bloques_info = {
    "madera": {"imagen": imagen_madera, "resistencia": 50},
    "concreto": {"imagen": imagen_concreto, "resistencia": 100},
    "acero": {"imagen": imagen_acero, "resistencia": 200}
}

# Botones para seleccionar tipos de bloques
boton_madera = pygame.Rect(50, 10, 100, 50)
boton_concreto = pygame.Rect(170, 10, 115, 50)
boton_acero = pygame.Rect(305, 10, 100, 50)

# Texto para las etiquetas
font = pygame.font.Font(None, 36)
etiqueta_madera = font.render("", True, WHITE)
etiqueta_concreto = font.render("", True, WHITE)
etiqueta_acero = font.render("", True, WHITE)

etiquetas = {
    "": (etiqueta_madera, (55, 20)),
    "": (etiqueta_concreto, (175, 20)),
    "": (etiqueta_acero, (320, 20))
}

# Lista de botones
botones = [boton_madera, boton_concreto, boton_acero]


#OKbjeto que limita los FPS, para asegurar una velocidad equilibrada
clock = pygame.time.Clock()

global atacante
global defensor

# Crea una instancia de Atacante y Defensor y pasa una tupla de coordenadas para definir la posición inicial en la pantalla
atacante = Atacante((screen_width // 15, screen_height // 7))
defensor = Defensor((screen_width // 3, screen_height // 3))

# Asigna el rol a cada personaje
atacante.rol = "Atacante"
defensor.rol = "Defensor"

# Color de la banda superior
banda_color = (26, 101, 156)

# Altura de la banda superior
banda_alto = 100

# Obtiene el tamaño de la pantalla del sistema
ventana_ancho, ventana_alto = pygame.display.Info().current_w, pygame.display.Info().current_h

bloques_colocados = []


#///////////////////guardar partida/////////////////////////
def message_screen_save(message, font, color, y_displacement=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2 + y_displacement)
    screen.blit(text, text_rect)
    
    
    # función de pantalla de guardar
def save():
    white = (255, 255, 255)
    
    # Cargar la imagen de fondo
    fondo = pygame.image.load("loginImages/fondo_reducido.png")
    
    #Función de pausar el juego
    save = True
    while save:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    save = False
                elif event.key == pygame.K_q:
                    save = False
                    salir()
                               
            screen.blit(fondo, (0,0))
            
            message_screen_save("Battle City",
                    fuente_pausa_2,
                    white,
                    -300)
            
            message_screen_save("Juego Guardado",
                        fuente_pausa_1,
                        white,
                        -100)
            message_screen_save("Presiona V para reanudar o Q para salir",
                        fuente_pausa_1,
                        white,
                        25)
            pygame.display.update()
            clock.tick(5) 
            
            
# Función para guardar partida
def guardar_partida():
    datos_partida = {
        "nombre_atacante": atacante_name,
        "nonbre_defensor": defensor_name, 
        "posicion_atacante": atacante.obtener_posicion_A(),
        "posicion_defensor": defensor.obtener_posicion_D(),
        "bloques_colocados": bloques_colocados,
        "bloques_restantes": bloques_restantes,  
        "municiones_restantes": atacante.municiones_restantes,  
        "bloques_usados": sum(bloques_creados.values())  
        # Otros datos de la partida...
    }
    
     # Ruta del archivo donde se guardará la partida
    archivo_partida = "partida.json"

    # Guardar los datos en el archivo JSON
    with open(archivo_partida, 'w') as archivo:
        json.dump(datos_partida, archivo)
        print("datos guardados")


"""
# Función para cargar partida
def cargar_partida():
    archivo_partida = "partida.json"
    try:
        with open(archivo_partida, 'r') as archivo:
            datos_partida = json.load(archivo)
        return datos_partida
    except FileNotFoundError:
        # Manejar la excepción si el archivo no existe
        return None

# Cuando quieras cargar la partida
datos_cargados = cargar_partida()
if datos_cargados:
    # Procesar los datos para restaurar la partida
    if "posicion_atacante" in datos_cargados:
        posicion_atacante = datos_cargados["posicion_atacante"]
        atacante = Atacante(posicion_atacante)

    if "posicion_defensor" in datos_cargados:
        posicion_defensor = datos_cargados["posicion_defensor"]
        defensor = Defensor(posicion_defensor)

    if "bloques_colocados" in datos_cargados:
        bloques_colocados = datos_cargados["bloques_colocados"]

    # Puedes restaurar otros datos como la munición, etc.

    # Continuar con el juego restaurado
else:
    
    # Manejar el caso en el que no se encuentra una partida guardada
    # Puedes crear nuevos personajes y configuraciones iniciales aquí si no hay datos guardados
    atacante = Atacante((screen_width // 2, screen_height // 2))
    defensor = Defensor((screen_width // 3, screen_height // 3))
    bloques_colocados = {}  # Inicializar bloques en blanco o con datos iniciales
    # Resto de la configuración inicial del juego
"""

##########################################################
   
start_time = pygame.time.get_ticks()

########################################################## 
if __name__ == "__main__":
    # Bucle principal del juego
    animacion = None
    while True:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
           
            # Manejar eventos de teclado
            keys = pygame.key.get_pressed()
            if keys[K_e]:
                atacante.cambiar_tipo_munición("fuego")
            elif keys[K_q]:
                atacante.cambiar_tipo_munición("hielo")
            elif keys[K_r]:
                atacante.cambiar_tipo_munición("bomba")
            if keys[K_b]:
                guardar_partida()
                save()
                
            if keys[K_m]:
                pause()

            if keys[K_x]:
                ventana_ayuda()

            if keys[K_p]:
                defensor.cambiar_tipo_bloque("p")
            elif keys[K_o]:
                defensor.cambiar_tipo_bloque("o")
            elif keys[K_u]:
                defensor.cambiar_tipo_bloque("u")
            elif keys[K_h]:
                if not defensor.alcanzado_limite_bloques():
                    defensor.colocar_bloque()

            if keys[K_g]:
                tiempo_restante = 1


        # Dibujar fondo, e imágenes de defensor, atacante, y botón de pausa.
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg, (0, 0))
        atacante.dibujar()
        defensor.dibujar()


        atacante.regenerar_municiones()
        mostrar_temporizador(screen)

        
        if tiempo_restante <= 0:
            reproducir_nueva_cancion()
            mostrar_temporizador2(screen)
        



        font = pygame.font.Font(None, 25)
        x = screen.get_width() - 10 - font.size("Texto muy largo")[0]  # Ajusta el espacio de margen deseado
        y = 10  # Ajusta la posición vertical si es necesario

        for tipo, cantidad in atacante.municiones_restantes.items():
            tipo_capitalizado = tipo.capitalize()  # Convierte la primera letra en mayúscula
            text = font.render(f'{tipo_capitalizado} : {cantidad}', True, WHITE)
            screen.blit(text, (x, y))
            y += 30  # Ajusta el espaciado vertical si es necesario

        # Dibujar los bloques y botones

       


        # Utiliza la misma fuente que se usa para las etiquetas
        font = pygame.font.Font(None, 25)

        # Dibujar etiquetas
        for texto, (x, y) in etiquetas.values():
            screen.blit(texto, (x, y))

        font = pygame.font.Font(None, 25)
        screen_width, screen_height = screen.get_size()  # Obtiene el ancho y alto de la pantalla



 
        # Dibujar los nombres de usuario
        font = pygame.font.Font(None, 30) 
        color = (255, 255, 255) 

        # colocar el nombre de usuario del atacante sobre el tanque
        if tiempo_restante == 0:
            text = font.render(atacante_name, True, color) 
            text_rect = text.get_rect()
            text_rect.midtop = (atacante.rect.centerx + 10, atacante.rect.top - 30)
            screen.blit(text, text_rect)
        
        # Colocar el nombre de usuario del defensor sobre el águila
        text = font.render(defensor_name, True, color) 
        text_rect = text.get_rect()
        text_rect.midtop = (defensor.rect.centerx, defensor.rect.top - 20) 
        screen.blit(text, text_rect)
        
        dx, dy = 0, 0 #Inicializa la dirección del Atacante en 0 para "x" y "y"

        # Mover Atacante 3px en eje "x/y"
        if tiempo_restante == 0:
            if keys[K_a]:
                dx = -3
                atacante.cambiar_direccion("left")
            if keys[K_d]:
                dx = 3
                atacante.cambiar_direccion("right")
            if keys[K_w]:
                dy = -3
                atacante.cambiar_direccion("up")
            if keys[K_s]:
                dy = 3
                atacante.cambiar_direccion("down")
            if keys[K_w] and keys[K_a]:
                dx, dy = -3, -3
                atacante.cambiar_direccion("ul")
            if keys[K_w] and keys[K_d]:
                dx, dy = 3, -3
                atacante.cambiar_direccion("ur")
            if keys[K_s] and keys[K_a]:
                dx, dy = -3, 3
                atacante.cambiar_direccion("dl")
            if keys[K_s] and keys[K_d]:
                dx, dy = 3, 3
                atacante.cambiar_direccion("dr")

            if dx != 0 or dy != 0: #Si la posición actual es diferente a la nueva instruccion, entonces se mueve el personaje
                atacante.mover(dx, dy)
                atacante.actualizar_frame()

        dr, dz = 0, 0 #Inicializa la dirección del Defensor en 0 para "x" y "y"

        # Mover Defensor 3px en eje "x/y"
        if keys[K_j]:
            dr = -3
            defensor.cambiar_direccion("left")
        if keys[K_l]:
            dr = 3
            defensor.cambiar_direccion("right")
        if keys[K_i]:
            dz = -3
            defensor.cambiar_direccion("up")
        if keys[K_k]:
            dz = 3
            defensor.cambiar_direccion("down")
        if keys[K_i] and keys[K_j]:
            dr, dz = -3, -3
            defensor.cambiar_direccion("ul")
        if keys[K_i] and keys[K_l]:
            dr, dz = 3, -3
            defensor.cambiar_direccion("ur")
        if keys[K_k] and keys[K_j]:
            dr, dz = -3, 3
            defensor.cambiar_direccion("dl")
        if keys[K_k] and keys[K_l]:
            dr, dz = 3, 3
            defensor.cambiar_direccion("dr")

        if dr != 0 or dz != 0: #Si la posición actual es diferente a la nueva instruccion, entonces se mueve el personaje
            defensor.mover(dr, dz)
            defensor.actualizar_frame()
            if defensor.vida <= 0:
                defensor.desaparecer()
        # Disparar
        if tiempo_restante == 0:
            if keys[K_SPACE]:
                atacante.disparar()

        if tiempo_restante2 == 1:
            pygame.mixer.music.stop()
            from pantalla_victoria import obtener_canciones_defensor
            pantalla_victoria(defensor_name)
            obtener_canciones_defensor(defensor_name)

        # Mover y actualizar las balas
        for bullet in atacante.bullets[:]:
            if bullet.esta_en_pantalla():
                bullet.mover()
                bullet.rect.topleft = (bullet.rect.topleft[0], bullet.rect.topleft[1])
                screen.blit(bullet.image, bullet.rect)



                if defensor.rect.colliderect(bullet.rect):
                    defensor.impacto(atacante.current_municion)
                    atacante.bullets.remove(bullet)

                for bloque in defensor.bloques:
                    if bloque.rect.colliderect(bullet.rect):
                        tipo_proyectil = bullet.__class__.__name__
                        bloque.impacto(tipo_proyectil)
                        atacante.bullets.remove(bullet)


            if not bullet.esta_en_pantalla():
                posicion_bala = bullet.rect.topleft  # Guarda la posición antes de eliminar la bala
                atacante.bullets.remove(bullet)


        if animacion:
            if animacion.actualizar():
                screen.blit(animacion.image, animacion.rect)
            else:
                animacion = None

        for bala in atacante.bullets:
    # Verificar colisiones con el Defensor
            if bala.rect.colliderect(defensor.rect):
                tipo_proyectil = bala.__class__.__name__  # Obtener el tipo de proyectil
                defensor.impacto(tipo_proyectil)  # Aplicar impacto al Defensor
                atacante.bullets.remove(bala) 

        for bloque in defensor.bloques[:]:
            bloque.dibujar(screen)
            if bloque.vida <= 0:
                defensor.bloques.remove(bloque)

        # actualizar pantalla completa
        pygame.display.flip()

        # velocidad de fotogramas a 60 fps
        clock.tick(60)


        
# Cuando quieras guardar la partida
guardar_partida()