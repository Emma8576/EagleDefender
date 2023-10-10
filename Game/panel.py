import pygame
import sys
import time
from pygame.locals import *

pygame.init()

# Obtener información de pantalla y ajustar a pantalla completa
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN)

# Cargar background
bg = [pygame.image.load(f"panel_elements/bg/frame-{i}.gif") for i in range(1, 24)]

# Clase base para los personajes
class Personaje:
    def __init__(self, image_paths, start_pos):
        self.images = {
            "up": [pygame.image.load(image_path) for image_path in image_paths["up"]],
            "down": [pygame.image.load(image_path) for image_path in image_paths["down"]],
            "right": [pygame.image.load(image_path) for image_path in image_paths["right"]],
            "left": [pygame.image.load(image_path) for image_path in image_paths["left"]],
            "ul": [pygame.image.load(image_path) for image_path in image_paths["ul"]],
            "ur": [pygame.image.load(image_path) for image_path in image_paths["ur"]],
            "dl": [pygame.image.load(image_path) for image_path in image_paths["dl"]],
            "dr": [pygame.image.load(image_path) for image_path in image_paths["dr"]],
        }

        self.current_frame = 0
        self.rect = self.images["up"][0].get_rect()
        self.rect.topleft = start_pos
        self.direction = "up"

    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect

    def draw(self):
        screen.blit(self.images[self.direction][self.current_frame], self.rect)

    def change_direction(self, new_direction):
        self.direction = new_direction

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])

# Clase Atacante
class Atacante(Personaje):
    def __init__(self, start_pos):
        image_paths = {
            "up": [f"panel_elements/atacante_sprites/atacante_up/frame-{i}.gif" for i in range(1, 5)],
            "down": [f"panel_elements/atacante_sprites/atacante_down/frame-{i}.gif" for i in range(1, 5)],
            "right": [f"panel_elements/atacante_sprites/atacante_right/frame-{i}.gif" for i in range(1, 5)],
            "left": [f"panel_elements/atacante_sprites/atacante_left/frame-{i}.gif" for i in range(1, 5)],
            "ul": [f"panel_elements/atacante_sprites/atacante_ul/frame-{i}.png" for i in range(1, 5)],
            "ur": [f"panel_elements/atacante_sprites/atacante_ur/frame-{i}.png" for i in range(1, 5)],
            "dl": [f"panel_elements/atacante_sprites/atacante_dl/frame-{i}.png" for i in range(1, 5)],
            "dr": [f"panel_elements/atacante_sprites/atacante_dr/frame-{i}.png" for i in range(1, 5)],
        }
        super().__init__(image_paths, start_pos)

# Clase Defensor
class Defensor(Personaje):
    def __init__(self, start_pos):
        image_paths = {
            "up": [f"panel_elements/defensor_sprites/defensor_up/frame-{i}.gif" for i in range(1, 9)],
            "down": [f"panel_elements/defensor_sprites/defensor_down/frame-{i}.gif" for i in range(1, 9)],
            "right": [f"panel_elements/defensor_sprites/defensor_right/frame-{i}.gif" for i in range(1, 9)],
            "left": [f"panel_elements/defensor_sprites/defensor_left/frame-{i}.gif" for i in range(1, 9)],
            "ul": [f"panel_elements/defensor_sprites/defensor_ul/frame-{i}.png" for i in range(1, 9)],
            "ur": [f"panel_elements/defensor_sprites/defensor_ur/frame-{i}.png" for i in range(1, 9)],
            "dl": [f"panel_elements/defensor_sprites/defensor_dl/frame-{i}.png" for i in range(1, 9)],
            "dr": [f"panel_elements/defensor_sprites/defensor_dr/frame-{i}.png" for i in range(1, 9)],
        }
        super().__init__(image_paths, start_pos)

clock = pygame.time.Clock()

# Crea una instancia de Atacante y Defensor
atacante = Atacante((screen_width // 2, screen_height // 2))
defensor = Defensor((screen_width // 3, screen_height // 3))

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0

    if keys[K_a]:
        dx = -5
        atacante.change_direction("left")
    if keys[K_d]:
        dx = 5
        atacante.change_direction("right")
    if keys[K_w]:
        dy = -5
        atacante.change_direction("up")
    if keys[K_s]:
        dy = 5
        atacante.change_direction("down")
    if keys[K_w] and keys[K_a]:
        dx, dy = -5, -5
        atacante.change_direction("ul")
    if keys[K_w] and keys[K_d]:
        dx, dy = 5, -5
        atacante.change_direction("ur")
    if keys[K_s] and keys[K_a]:
        dx, dy = -5, 5
        atacante.change_direction("dl")
    if keys[K_s] and keys[K_d]:
        dx, dy = 5, 5
        atacante.change_direction("dr")

    if dx != 0 or dy != 0:
        atacante.move(dx, dy)
        atacante.update_frame()

    dr, dz = 0, 0

    if keys[K_j]:
        dr = -5
        defensor.change_direction("left")
    if keys[K_l]:
        dr = 5
        defensor.change_direction("right")
    if keys[K_i]:
        dz = -5
        defensor.change_direction("up")
    if keys[K_k]:
        dz = 5
        defensor.change_direction("down")
    if keys[K_i] and keys[K_j]:
        dr, dz = -5, -5
        defensor.change_direction("ul")
    if keys[K_i] and keys[K_l]:
        dr, dz = 5, -5
        defensor.change_direction("ur")
    if keys[K_k] and keys[K_j]:
        dr, dz = -5, 5
        defensor.change_direction("dl")
    if keys[K_k] and keys[K_l]:
        dr, dz = 5, 5
        defensor.change_direction("dr")

    if dr != 0 or dz != 0:
        defensor.move(dr, dz)
        defensor.update_frame()

    frame = int(time.time() * 10) % len(bg)

    screen.blit(bg[frame], (0, 0))
    
    atacante.draw()
    defensor.draw()

    pygame.display.flip()
    clock.tick(60)
