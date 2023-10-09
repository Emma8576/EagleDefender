import pygame
import sys
from pygame import *
import time

pygame.init()
#Obtener información de pantalla y ajustar a pantalla completa
screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = display.set_mode((screen_width, screen_height), FULLSCREEN)

#Cargar background
bg = []

for i in range(1, 24):
    nombre_bg = f"panel_elements/bg/frame-{i}.gif"
    bg.append(image.load(nombre_bg))

#Clase que va a definir atributos y comportamiento del usuario Atacante
class Atacante:
    def __init__(self): #Iniciación del método constructor
    	# Inicialización de listas para almacenar frames de diferentes direcciones.
    	# Cada lista representa una dirección de movimiento
        self.images_up = []  # Dirección hacia arriba
        self.images_down = []  # Dirección hacia abajo
        self.images_right = []  # Dirección hacia la derecha
        self.images_left = []  # Dirección hacia la izquierda
        self.images_ul = []  # Dirección arriba-izquierda
        self.images_ur = []  # Dirección arriba-derecha
        self.images_dl = []  # Dirección abajo-izquierda
        self.images_dr = []  # Dirección abajo-derecha

        #bucle para cargar las imágenes en cada dirección mediante variables, cada directorio contiene 4 sprites
        for i in range(1, 5): 
            nombre_img_up = f"panel_elements/atacante_sprites/atacante_up/frame-{i}.gif"
            nombre_img_down = f"panel_elements/atacante_sprites/atacante_down/frame-{i}.gif"
            nombre_img_right = f"panel_elements/atacante_sprites/atacante_right/frame-{i}.gif"
            nombre_img_left = f"panel_elements/atacante_sprites/atacante_left/frame-{i}.gif"
            nombre_img_ul = f"panel_elements/atacante_sprites/atacante_ul/frame-{i}.png"
            nombre_img_ur = f"panel_elements/atacante_sprites/atacante_ur/frame-{i}.png"
            nombre_img_dl = f"panel_elements/atacante_sprites/atacante_dl/frame-{i}.png"
            nombre_img_dr = f"panel_elements/atacante_sprites/atacante_dr/frame-{i}.png"


            # Fragmento que carga cada sprite dentro de las listas correspondientes ya definidas mediante método append()
            # Se cargan respectivamente a como fueron cargadas en la definición de las listas vacías
            self.images_up.append(image.load(nombre_img_up))
            self.images_down.append(image.load(nombre_img_down))
            self.images_right.append(image.load(nombre_img_right))
            self.images_left.append(image.load(nombre_img_left))
            self.images_ul.append(image.load(nombre_img_ul))
            self.images_ur.append(image.load(nombre_img_ur))
            self.images_dl.append(image.load(nombre_img_dl))
            self.images_dr.append(image.load(nombre_img_dr))

        self.current_frame = 0 # variable que inicia el primer elemento de la lista, es decir, la primer imagen
        self.rect = self.images_up[0].get_rect() # variable que almacena la creación de un rectángulo del tamaño del tanque para detectar movimiento y colisiones
        self.rect.topleft = (screen_width//2, screen_height//2) # Acomoda de manera predeterminada en tanque sobre la pantalla
        self.direction = "up" # Establece dirección predeterminada


    #Función encargada de mantener el tanque dentro de la pantalla, no puede salir de los bordes
    #Calcula la nueva posición del rectángulo, luego comprueba si la dirección está dentro de la pantalla y si está dentro actualiza la nueva posición 
    def mover_atacante(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect


    # Función que dibuja de manera adecuada el tanque basado en la dirección
    # Si la dirección es ___ entonces carga _<variable con la lista vacía>_
    def dibujar_atacante(self):
        if self.direction == "up":
    	    screen.blit(self.images_up[self.current_frame], self.rect)
        elif self.direction == "down":
    	    screen.blit(self.images_down[self.current_frame], self.rect)
        elif self.direction == "right":
    	    screen.blit(self.images_right[self.current_frame], self.rect)
        elif self.direction == "left":
    	    screen.blit(self.images_left[self.current_frame], self.rect)
        elif self.direction == "ul": 
             screen.blit(self.images_ul[self.current_frame], self.rect)
        elif self.direction == "ur":
            screen.blit(self.images_ur[self.current_frame], self.rect)
        elif self.direction == "dl":
            screen.blit(self.images_dl[self.current_frame], self.rect)
        elif self.direction == "dr":
            screen.blit(self.images_dr[self.current_frame], self.rect)

    #cambia la dirección del tanque según la tecla presionada en cada iteración
    def cambiar_direccion_atacante(self, nueva_direccion):
    	self.direction = nueva_direccion    	

    # Actualiza el índice de la imagen actual, increementando el índice y ajustando el rango válido mediante el operando % (es decir, divide entre la cantidad de sprites del directorio)
    def actualizar_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images_up)

#Clase que define los atributos y comportamientos del usuario Defensor
class Defensor:
    def __init__(self):
        # Inicialización de listas para almacenar frames de diferentes direcciones.
        # Cada lista representa una dirección de movimiento
        self.images_up = []  # Dirección hacia arriba
        self.images_down = []  # Dirección hacia abajo
        self.images_right = []  # Dirección hacia la derecha
        self.images_left = []  # Dirección hacia la izquierda
        self.images_ul = []  # Dirección arriba-izquierda
        self.images_ur = []  # Dirección arriba-derecha
        self.images_dl = []  # Dirección abajo-izquierda
        self.images_dr = []  # Dirección abajo-derecha

        # bucle para cargar las imágenes en cada dirección mediante variables, cada directorio contiene 4 sprites
        for i in range(1, 9): 
            nombre_img_up = f"panel_elements/defensor_sprites/defensor_up/frame-{i}.gif"
            nombre_img_down = f"panel_elements/defensor_sprites/defensor_down/frame-{i}.gif"
            nombre_img_right = f"panel_elements/defensor_sprites/defensor_right/frame-{i}.gif"
            nombre_img_left = f"panel_elements/defensor_sprites/defensor_left/frame-{i}.gif"
            nombre_img_ul = f"panel_elements/defensor_sprites/defensor_ul/frame-{i}.png"
            nombre_img_ur = f"panel_elements/defensor_sprites/defensor_ur/frame-{i}.png"
            nombre_img_dl = f"panel_elements/defensor_sprites/defensor_dl/frame-{i}.png"
            nombre_img_dr = f"panel_elements/defensor_sprites/defensor_dr/frame-{i}.png"

            # Fragmento que carga cada sprite dentro de las listas correspondientes ya definidas mediante método append()
            # Se cargan respectivamente a como fueron cargadas en la definición de las listas vacías
            self.images_up.append(image.load(nombre_img_up))
            self.images_down.append(image.load(nombre_img_down))
            self.images_right.append(image.load(nombre_img_right))
            self.images_left.append(image.load(nombre_img_left))
            self.images_ul.append(image.load(nombre_img_ul))
            self.images_ur.append(image.load(nombre_img_ur))
            self.images_dl.append(image.load(nombre_img_dl))
            self.images_dr.append(image.load(nombre_img_dr))

        self.current_frame = 0  # variable que inicia el primer elemento de la lista, es decir, la primer imagen
        self.rect = self.images_up[0].get_rect()  # variable que almacena la creación de un rectángulo del tamaño del tanque para detectar movimiento y colisiones
        self.rect.topleft = (screen_width // 3, screen_height // 3)  # Acomoda de manera predeterminada en tanque sobre la pantalla
        self.direction = "up"  # Establece dirección predeterminada



    def mover_defensor(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect

    # Función que dibuja de manera adecuada el tanque basado en la dirección
    # Si la dirección es ___ entonces carga _<variable con la lista vacía>_
    def dibujar_defensor(self):
        if self.direction == "up":
    	    screen.blit(self.images_up[self.current_frame], self.rect)
        elif self.direction == "down":
    	    screen.blit(self.images_down[self.current_frame], self.rect)
        elif self.direction == "right":
    	    screen.blit(self.images_right[self.current_frame], self.rect)
        elif self.direction == "left":
    	    screen.blit(self.images_left[self.current_frame], self.rect)
        elif self.direction == "ul": 
             screen.blit(self.images_ul[self.current_frame], self.rect)
        elif self.direction == "ur":
            screen.blit(self.images_ur[self.current_frame], self.rect)
        elif self.direction == "dl":
            screen.blit(self.images_dl[self.current_frame], self.rect)
        elif self.direction == "dr":
            screen.blit(self.images_dr[self.current_frame], self.rect)

    #cambia la dirección del tanque según la tecla presionada en cada iteración
    def cambiar_direccion_defensor(self, nueva_direccion):
    	self.direction = nueva_direccion    	

    # Actualiza el índice de la imagen actual, increementando el índice y ajustando el rango válido mediante el operando % (es decir, divide entre la cantidad de sprites del directorio)
    def actualizar_frame_defensor(self):
        self.current_frame = (self.current_frame + 1) % len(self.images_up)

    #Fin ejecución clase Defensor





clock = pygame.time.Clock()

# Crea una instancia de atacante
atacante = Atacante()
defensor = Defensor()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Variable que almacena la tecla presionada
    keys = pygame.key.get_pressed()

    dx, dy = 0, 0 # Se inicializa la dirección en posición nula
    

    #Se configura comportamiento de imagen según la tecla presionada
    # Ej: Si la tecla es A, se mueve 5 pixeles a la izquierda y cambia de dirección con la imagen corresepondiente
    if keys[K_a]:
        dx = -5
        atacante.cambiar_direccion_atacante("left")
    if keys[K_d]:
        dx = 5
        atacante.cambiar_direccion_atacante("right")
    if keys[K_w]:
        dy = -5
        atacante.cambiar_direccion_atacante("up")
    if keys[K_s]:
        dy = 5
        atacante.cambiar_direccion_atacante("down")
    if keys[K_w] and keys[K_a]:
    	dx, dy = -5,-5
    	atacante.cambiar_direccion_atacante("ul")
    if keys[K_w] and keys[K_d]:
    	dx, dy = 5, -5
    	atacante.cambiar_direccion_atacante("ur")
    if keys[K_s] and keys[K_a]:
    	dx, dy = -5,5
    	atacante.cambiar_direccion_atacante("dl")
    if keys[K_s] and keys[K_d]:
    	dx, dy = 5,5
    	atacante.cambiar_direccion_atacante("dr")

    #si dx o dy es diferente de 0, llama a la función mover_atacante() para mover la imagen según la dirección deseada dentro del rango de los sprites mediante actualizar_frame()
    if dx != 0 or dy != 0:
        atacante.mover_atacante(dx, dy)
        atacante.actualizar_frame()

    dr, dz = 0, 0

    if keys[K_j]:
        dr = -5
        defensor.cambiar_direccion_defensor("left")
    if keys[K_l]:
        dr = 5
        defensor.cambiar_direccion_defensor("right")
    if keys[K_i]:
        dz = -5
        defensor.cambiar_direccion_defensor("up")
    if keys[K_k]:
        dz = 5
        defensor.cambiar_direccion_defensor("down")
    if keys[K_i] and keys[K_j]:
    	dr, dz = -5,-5
    	defensor.cambiar_direccion_defensor("ul")
    if keys[K_i] and keys[K_l]:
    	dr, dz = 5, -5
    	defensor.cambiar_direccion_defensor("ur")
    if keys[K_k] and keys[K_j]:
    	dr, dz = -5,5
    	defensor.cambiar_direccion_defensor("dl")
    if keys[K_k] and keys[K_l]:
    	dr, dz = 5,5
    	defensor.cambiar_direccion_defensor("dr")

    if dr != 0 or dz != 0:
        defensor.mover_defensor(dr, dz)
        defensor.actualizar_frame_defensor()


    #Ajusta parámetros del background
    frame = int(time.time()*10) 
    frame %= len(bg)

    screen.blit(bg[frame], (0, 0))
    #................................

    atacante.dibujar_atacante() # Llama al método dibujar_atacante para mostrar la imagen del tanque, dependiendo de la dirección  
    defensor.dibujar_defensor()

    pygame.display.flip()
    clock.tick(60)#Se establece bucle principal a 60 frames por segundo

pygame.quit() # Fin de ejecución del programa
