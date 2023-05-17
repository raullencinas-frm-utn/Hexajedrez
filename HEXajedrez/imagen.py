import pygame

class Imagen:
    def __init__(self, direccion):
        self.anchoPantalla = 1100
        self.altoPantalla = 700
        self.imagen = pygame.image.load(direccion).convert_alpha()
        self.direccion = direccion
        
    def redimensionar(self, x, y):
        self.imagen = pygame.transform.scale(self.imagen,(x, y))
        return self.imagen
    
    def obtenerImagen(self):
        return self.imagen
        