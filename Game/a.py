import pygame
import sys

# Inicializar pygame
pygame.init()
# Crear una ventana de 800x600 píxeles
window = pygame.display.set_mode((800, 600))
# Establecer el título de la ventana
pygame.display.set_caption("Ejemplo de botón")

# Definir una clase para representar un botón
class Button:
    # El constructor recibe el texto, el color, la posición y el tamaño del botón
    def __init__(self, text, color, x, y, width, height):
        # Crear una fuente para renderizar el texto
        self.font = pygame.font.SysFont("Arial", 32)
        # Crear una superficie con el texto y el color dados
        self.text = self.font.render(text, True, color)
        # Obtener el rectángulo que contiene la superficie del texto
        self.text_rect = self.text.get_rect()
        # Centrar el rectángulo del texto en la posición y el tamaño dados
        self.text_rect.center = (x + width // 2, y + height // 2)
        # Crear un rectángulo con la posición y el tamaño dados
        self.rect = pygame.Rect(x, y, width, height)

    # Definir un método para dibujar el botón en la ventana
    def draw(self, window):
        # Dibujar el rectángulo del botón en la ventana
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        # Dibujar el texto del botón en la ventana
        window.blit(self.text, self.text_rect)

    # Definir un método para comprobar si el botón ha sido pulsado
    def is_pressed(self, mouse_pos, mouse_click):
        # Comprobar si la posición del ratón está dentro del rectángulo del botón
        if self.rect.collidepoint(mouse_pos):
            # Comprobar si se ha hecho clic con el botón izquierdo del ratón
            if mouse_click[0]:
                # Devolver True si se cumplen ambas condiciones
                return True
        # Devolver False si no se cumplen las condiciones
        return False

# Crear un botón con el texto "Hola", el color rojo, y la posición y el tamaño indicados
button = Button("Hola", (255, 0, 0), 300, 200, 200, 100)

# Crear un reloj para controlar el tiempo
clock = pygame.time.Clock()
# Crear una variable para el bucle principal
running = True

# Bucle principal
while running:
    # Limitar la velocidad de fotogramas a 60 FPS
    clock.tick(60)
    # Obtener la posición y el estado del ratón
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    # Recorrer los eventos de pygame
    for event in pygame.event.get():
        # Si se cierra la ventana, salir del bucle
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        # Si se pulsa el botón, imprimir un mensaje
        if button.is_pressed(mouse_pos, mouse_click):
            print("Has pulsado el botón")

    # Rellenar la ventana con el color negro
    window.fill((0, 0, 0))
    # Dibujar el botón en la ventana
    button.draw(window)
    # Actualizar la ventana
    pygame.display.update()
