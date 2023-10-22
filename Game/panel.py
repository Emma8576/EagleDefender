"""Código mantenido por Bryan Monge - 2023026192"""

import pygame
import sys
import time
from pygame import *
import subprocess
import os

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
# Cargar la fuente texto
fuente_pausa_1 = pygame.font.Font(ruta_fuente, tamaño_fuente_texto)
# Cargar la fuente titulo
fuente_pausa_2 = pygame.font.Font(ruta_fuente, tamaño_fuente_titulo)

#Se cargan los sonidos que se ejecutan según el tipo de munición disparada
pygame.mixer.init()
agua = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/agua.wav")
fuego = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/fuego.wav")
bomba = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/bomba.wav")
# Cargar background
bg = pygame.image.load("panel_elements/bg/bag.jpg") 

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
def message_screen(message, font, color, y_displacement=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 2 + y_displacement)
    screen.blit(text, text_rect)
    
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
                    subprocess.run(["python", "Login.py"])
                    sys.exit()
                               
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
            pygame.display.update()
            clock.tick(5)
            
# Ejemplo de lectura de roles desde un archivo de texto
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

# Imprimir el rol del Defensor
if 'Defensor' in roles:
    print('Rol del Defensor:', roles['Defensor'])

# Prueba: Imprimir el rol del Atacante
if 'Atacante' in roles:
    print('Rol del Atacante:', roles['Atacante'])
           
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
        },0.9)

        self.current_frame = 0
        self.rect = self.images["up"][0].get_rect() #Rectángulo para detectar posicionamiento y colisiones
        self.rect.topleft = start_pos
        self.direction = "up"
    #Mueve al personaje en el eje "x" y "y"
    def mover(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect): #Mantiene el personaje dentro de la pantalla
            self.rect = new_rect
    #Dibuja al personaje en la direccion actual
    def dibujar(self):
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
        #cambia el tipo de saldo
    def cambiar_tipo_munición(self, tipo):
        self.current_municion = tipo

    #Dispara un proyectil en la dirección actual
    def disparar(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000: #Intervalo de un segundo por disparo
            self.last_shot_time = current_time
            municion = self.municiones[self.current_municion]
            bullet = municion(self.rect.topleft, self.direction)
            self.bullets.append(bullet)
            #Reproduce los sonidos por cada tipo de munición
            if self.current_municion == "agua":
                self.agua.play()
            elif self.current_municion == "fuego":
                self.fuego.play()
            elif self.current_municion == "bomba":
                self.bomba.play()
                
#Clase que representa el tipo de municion Fuego
class proyectilFuego:
    """Author: Bryan Monge
       start_pos: indica la posicíón inicial del proyectl
       direction: dirección inicial del proyectil

    """
    def __init__(self, start_pos, direction):
        self.images = escalar_imagenes ({ #diccionario que contiene las direcciones del proyectil
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_up/frame-{i}.gif") for i in range(1,16)],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_down/frame-{i}.gif") for i in range(1,16)],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_left/frame-{i}.gif") for i in range(1,16)],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_right/frame-{i}.gif") for i in range(1,16)],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(2,16)],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(2,16)],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(2,16)],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(2,16)],
        }, 0.5)


        self.direction = direction #Dirección del proyectil
        self.current_frame = 0
        self.image = self.images[direction][0] #Imagen actual del proyectil
        self.rect = self.image.get_rect() #Representa la posición y tamaño del proyectil
        self.rect.topleft = start_pos
        
    #Mueve el proyectil en la clase especificada
    #Si la dirección actual es __ entonces se mueve "x" y "y" unidades
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0,-6)
        elif self.direction == "down":
            self.rect.move_ip(0,6)
        elif self.direction == "left":
            self.rect.move_ip(-6,0)
        elif self.direction == "right":
            self.rect.move_ip(6,0)
        elif self.direction == "ul":
            self.rect.move_ip(-6,-6)
        elif self.direction == "ur":
            self.rect.move_ip(6,-6)
        elif self.direction == "dl":
            self.rect.move_ip(-6,6)
        elif self.direction == "dr":
            self.rect.move_ip(6,6)
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

    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)


# Clase que representa al personaje Defensor. Hereda de la clase Personake
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

#OKbjeto que limita los FPS, para asegurar una velocidad equilibrada
clock = pygame.time.Clock()

# Crea una instancia de Atacante y Defensor y pasa una tupla de coordenadas para definir la posición inicial en la pantalla
atacante = Atacante((screen_width // 2, screen_height // 2))
defensor = Defensor((screen_width // 3, screen_height // 3))

if __name__ == "__main__":
    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            # Manejar eventos de teclado
            keys = pygame.key.get_pressed()
            if keys[K_p]:
                atacante.cambiar_tipo_munición("fuego")
            elif keys[K_o]:
                atacante.cambiar_tipo_munición("hielo")
            elif keys[K_u]:
                atacante.cambiar_tipo_munición("bomba")

            if keys[K_m]:
                pause()
           
                    
        # Dibujar fondo, e imágenes de defensor, atacante, y botón de pausa.
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
        screen.blit(bg, (0, 0))
        atacante.dibujar()
        defensor.dibujar()
    

        

        dx, dy = 0, 0 #Inicializa la dirección del Atacante en 0 para "x" y "y"

        # Mover Atacante 3px en eje "x/y"
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

        # Disparar
        if keys[K_SPACE]:
            atacante.disparar()

        # Mover y actualizar las balas
        for bullet in atacante.bullets:
            bullet.mover()
            bullet.current_frame = (bullet.current_frame + 1) % len(bullet.images[bullet.direction])
            bullet.image = bullet.images[bullet.direction][bullet.current_frame]

            # Borrar balas que salen de la pantalla
            if not bullet.esta_en_pantalla():
                atacante.bullets.remove(bullet)
            else:
                # Dibujar balas en la pantalla
                screen.blit(bullet.image, bullet.rect)

        # actualizar pantalla completa
        pygame.display.flip()

        # velocidad de fotogramas a 60 fps
        clock.tick(60)
