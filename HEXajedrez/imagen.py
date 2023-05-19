import pygame

class Imagen:
    def __init__(self, direccion):
        """Constructor de una imagen."""
        self.anchoPantalla = 1100
        self.altoPantalla = 700
        self.imagen = pygame.image.load(direccion).convert_alpha()
        self.direccion = direccion
        
    def redimensionar(self, x, y):
        """Redimensiona la imagen."""
        self.imagen = pygame.transform.scale(self.imagen,(x, y))
        return self.imagen
    
    def obtenerImagen(self):
        """Devuelve la imagen en el formato reconocido por pygame."""
        return self.imagen
        