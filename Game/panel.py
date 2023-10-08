import pygame
import sys
from pygame import *
import time

pygame.init()

screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = display.set_mode((screen_width, screen_height), FULLSCREEN)

bg = []

for i in range(1, 24):
    nombre_bg = f"panel_elements/bg/frame-{i}.gif"
    bg.append(image.load(nombre_bg))

class Atacante:
    def __init__(self):
        self.images_up = []
        self.images_down = []
        self.images_right = []
        self.images_left = []
        self.images_ul = []
        self.images_ur = []
        self.images_dl = []
        self.images_dr = []

        for i in range(1, 5):
            nombre_img_up = f"panel_elements/atacante_up/frame-{i}.gif"
            nombre_img_down = f"panel_elements/atacante_down/frame-{i}.gif"
            nombre_img_right = f"panel_elements/atacante_right/frame-{i}.gif"
            nombre_img_left = f"panel_elements/atacante_left/frame-{i}.gif"
            nombre_img_ul = f"panel_elements/atacante_ul/frame-{i}.png"
            nombre_img_ur = f"panel_elements/atacante_ur/frame-{i}.png"
            nombre_img_dl = f"panel_elements/atacante_dl/frame-{i}.png"
            nombre_img_dr = f"panel_elements/atacante_dr/frame-{i}.png"

            self.images_up.append(image.load(nombre_img_up))
            self.images_down.append(image.load(nombre_img_down))
            self.images_right.append(image.load(nombre_img_right))
            self.images_left.append(image.load(nombre_img_left))
            self.images_ul.append(image.load(nombre_img_ul))
            self.images_ur.append(image.load(nombre_img_ur))
            self.images_dl.append(image.load(nombre_img_dl))
            self.images_dr.append(image.load(nombre_img_dr))

        self.current_frame = 0
        self.rect = self.images_up[0].get_rect()
        self.rect.topleft = (screen_width//2, screen_height//2)
        self.direction = "up"

    def mover(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect



    def dibujar(self):
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


    def cambiar_direccion(self, nueva_direccion):
    	self.direction = nueva_direccion    	

    def actualizar_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.images_up)



clock = pygame.time.Clock()

atacante = Atacante()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0

    if keys[K_a]:
        dx = -5
        atacante.cambiar_direccion("left")
    if keys[K_d]:
        dx = 5
        atacante.cambiar_direccion("right")
    if keys[K_w]:
        dy = -5
        atacante.cambiar_direccion("up")
    if keys[K_s]:
        dy = 5
        atacante.cambiar_direccion("down")
    if keys[K_w] and keys[K_a]:
    	dx, dy = -5,-5
    	atacante.cambiar_direccion("ul")
    if keys[K_w] and keys[K_d]:
    	dx, dy = 5, -5
    	atacante.cambiar_direccion("ur")
    if keys[K_s] and keys[K_a]:
    	dx, dy = -5,5
    	atacante.cambiar_direccion("dl")
    if keys[K_s] and keys[K_d]:
    	dx, dy = 5,5
    	atacante.cambiar_direccion("dr")


    if dx != 0 or dy != 0:
        atacante.mover(dx, dy)
        atacante.actualizar_frame()


    frame = int(time.time()*10)
    frame %= len(bg)

    screen.blit(bg[frame], (0, 0))

    atacante.dibujar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
#cartago
