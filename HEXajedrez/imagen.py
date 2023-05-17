import pygame

class Imagen:
    def __init__(self, direccion):
        self.anchoPantalla = 1100
        self.altoPantalla = 700
        self.imagen = pygame.image.load(direccion).convert_alpha()
        self.direccion = direccion
        
    def redimensionar(self, anchoPantalla, altoPantalla):
        tamañoImagen = self.imagen.get_rect()
        self.imagen = pygame.image.load(self.direccion).convert_alpha()
        KdePantalla = anchoPantalla / self.anchoPantalla
        x = tamañoImagen.width * (KdePantalla)
        y = tamañoImagen.height * (KdePantalla)
        self.anchoPantalla = anchoPantalla
        self.altoPantalla = altoPantalla
        self.imagen = pygame.transform.scale(self.imagen,(x, y))
        
        return self.imagen
    
    def obtenerImagen(self):
        return self.imagen
        