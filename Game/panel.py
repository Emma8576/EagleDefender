import pygame
import sys
import time
from pygame import *

pygame.init()
# Obtener información de pantalla y ajustar a pantalla completa
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)

pygame.mixer.init()
agua = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/agua.wav")
fuego = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/fuego.wav")
bomba = pygame.mixer.Sound("panel_elements/atacante_elementos/atacante_municion_sonidos/bomba.wav")
# Cargar background
bg = pygame.image.load("panel_elements/bg/bg.jpg") 

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
def pause():
    pausa = True
    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pausa = False
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pausa = False

# Clase base para los personajes
class Personaje:
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
        self.rect = self.images["up"][0].get_rect()
        self.rect.topleft = start_pos
        self.direction = "up"

    def mover(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect

    def dibujar(self):
        screen.blit(self.images[self.direction][self.current_frame], self.rect)

    def cambiar_direccion(self, new_direction):
        self.direction = new_direction

    def actualizar_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])

# Clase Atacante
class Atacante(Personaje):
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
        self.last_shot_time = 0
        self.bullets = []

        self.municiones = {"fuego": proyectilFuego, "hielo": proyectilHielo, "bomba": proyectilBomba}
        self.current_municion = "fuego"

        self.agua = agua
        self.fuego = fuego
        self.bomba = bomba

    def cambiar_tipo_munición(self, tipo):
        self.current_municion = tipo


    def disparar(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= 1000:
            self.last_shot_time = current_time
            municion = self.municiones[self.current_municion]
            bullet = municion(self.rect.topleft, self.direction)
            self.bullets.append(bullet)

            if self.current_municion == "agua":
                self.agua.play()
            elif self.current_municion == "fuego":
                self.fuego.play()
            elif self.current_municion == "bomba":
                self.bomba.play()

class proyectilFuego:
    def __init__(self, start_pos, direction):
        self.images = escalar_imagenes ({
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_up/frame-{i}.gif") for i in range(1,16)],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_down/frame-{i}.gif") for i in range(1,16)],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_left/frame-{i}.gif") for i in range(1,16)],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_right/frame-{i}.gif") for i in range(1,16)],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(1,16)],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(1,16)],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(1,16)],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/fuego/atacante_munición_ul/frame-{i}.gif") for i in range(1,16)],
        }, 0.5)


        self.direction = direction
        self.current_frame = 0
        self.image = self.images[direction][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        
        
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0,-8)
        elif self.direction == "down":
            self.rect.move_ip(0,8)
        elif self.direction == "left":
            self.rect.move_ip(-8,0)
        elif self.direction == "right":
            self.rect.move_ip(8,0)
        elif self.direction == "ul":
            self.rect.move_ip(-8,-8)
        elif self.direction == "ur":
            self.rect.move_ip(8,-8)
        elif self.direction == "dl":
            self.rect.move_ip(-8,8)
        elif self.direction == "dr":
            self.rect.move_ip(8,8)

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
            self.rect.move_ip(0,-8)
        elif self.direction == "down":
            self.rect.move_ip(0,8)
        elif self.direction == "left":
            self.rect.move_ip(-8,0)
        elif self.direction == "right":
            self.rect.move_ip(8,0)
        elif self.direction == "ul":
            self.rect.move_ip(-8,-8)
        elif self.direction == "ur":
            self.rect.move_ip(8,-8)
        elif self.direction == "dl":
            self.rect.move_ip(-8,8)
        elif self.direction == "dr":
            self.rect.move_ip(8,8)

    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)

class proyectilBomba:
    def __init__(self, start_pos, direction):
        self.images = {
            "up":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "down":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "left":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "right":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "ul":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "ur":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "dl":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
            "dr":[pygame.image.load(f"panel_elements/atacante_elementos/atacante_municion/bomba/frame-{i}.gif") for i in range(1,9)],
        }
        self.rect = self.images[direction][0].get_rect()
        self.rect.topleft = start_pos
        self.direction = direction
        self.current_frame = 0
        self.image = self.images[direction][0]
        
        
    def mover(self):
        if self.direction == "up":
            self.rect.move_ip(0,-8)
        elif self.direction == "down":
            self.rect.move_ip(0,8)
        elif self.direction == "left":
            self.rect.move_ip(-8,0)
        elif self.direction == "right":
            self.rect.move_ip(8,0)
        elif self.direction == "ul":
            self.rect.move_ip(-8,-8)
        elif self.direction == "ur":
            self.rect.move_ip(8,-8)
        elif self.direction == "dl":
            self.rect.move_ip(-8,8)
        elif self.direction == "dr":
            self.rect.move_ip(8,8)

    def esta_en_pantalla(self):
        return screen.get_rect().colliderect(self.rect)


# Clase Defensor
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


clock = pygame.time.Clock()

# Crea una instancia de Atacante y Defensor
atacante = Atacante((screen_width // 2, screen_height // 2))
defensor = Defensor((screen_width // 3, screen_height // 3))

# Imagenes botón pausa y play
imagen_pausa = pygame.image.load("panel_elements/pause_play_buttons/pause_button1.png")
imagen_play = pygame.image.load("panel_elements/pause_play_buttons/play_button.png")

# posición del botón de pausa
x,y = 10, 10

# Estado del juego
juego_pausado = False

running = True

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            #pygame.quit()
    # Dibujar fondo, e imágenes de defensor, atacante, y botón de pausa.
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    screen.blit(bg, (0, 0))
    atacante.dibujar()
    defensor.dibujar()
    screen.blit(imagen_pausa, (x, y))

    # Manejar eventos de teclado
    # Estado de las teclas
    keys = pygame.key.get_pressed()
    if keys[K_p]:
        atacante.cambiar_tipo_munición("fuego")
    elif keys[K_o]:
        atacante.cambiar_tipo_munición("hielo")
    elif keys[K_u]:
        atacante.cambiar_tipo_munición("bomba")

    if keys[K_m]:
        pause()
    pygame.display.update()


    dx, dy = 0, 0

    # Mover atacante
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

    if dx != 0 or dy != 0:
        atacante.mover(dx, dy)
        atacante.actualizar_frame()

    dr, dz = 0, 0

    # Mover defensor
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

    if dr != 0 or dz != 0:
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
