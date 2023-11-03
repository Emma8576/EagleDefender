import pygame

class AnimacionDestruccion:
    def __init__(self, start_pos):
        self.frames = [pygame.image.load(f"C:\\Users\\User\\OneDrive - Estudiantes ITCR\\Documentos\\EagleDefender\\Game\\panel_elements\\atacante_elementos\\atacante_municion\\municion_destruccion\\frame-{i}.gif") for i in range(1, 13)]
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos
        self.start_time = pygame.time.get_ticks()

    def actualizar(self):
	    current_time = pygame.time.get_ticks()

	    if current_time - self.start_time >= len(self.frames) * 50:
	        return False

	    self.current_frame = (current_time - self.start_time) // 50
	    self.image = self.frames[self.current_frame]

	    return True

