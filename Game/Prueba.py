import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ejemplo de Botón de Pausa")

# Carga las imágenes del botón de pausa y el botón de reproducción
pause_button_image = pygame.image.load('pause_button.png')
play_button_image = pygame.image.load('play_button.png')

# Escala las imágenes
button_size = (50, 50)
pause_button_image = pygame.transform.scale(pause_button_image, button_size)
play_button_image = pygame.transform.scale(play_button_image, button_size)

# Coordenadas del botón de pausa
button_x = 10
button_y = 10

# Estado inicial: reproducción
is_paused = False

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_x < event.pos[0] < button_x + button_size[0] and \
               button_y < event.pos[1] < button_y + button_size[1]:
                # El botón de pausa/reproducción se ha hecho clic
                is_paused = not is_paused

    screen.fill((255, 255, 255))

    # Dibuja el botón apropiado según el estado
    if is_paused:
        screen.blit(play_button_image, (button_x, button_y))
    else:
        screen.blit(pause_button_image, (button_x, button_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
