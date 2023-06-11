import pygame

class Imagen:
    def __init__(self, direccion):
        """Constructor de una imagen."""
        self.anchoPantalla, self.altoPantalla = pygame.display.get_surface().get_size()
        self.direccion = direccion
        self.imagen = pygame.image.load(direccion).convert_alpha()
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.rectangulo = self.imagen.get_rect() 

    def dibujar(self, x, y):
        """Dibuja la imagen en pantalla."""
        anchoPantalla, altoPantalla = pygame.display.get_surface().get_size()
        escala_x = anchoPantalla / self.anchoPantalla
        escala_y = altoPantalla / self.altoPantalla
        if escala_x > escala_y:
            escala = escala_y
        else:
            escala = escala_x
        if x!=0 and y !=0:
            x -= self.anchoPantalla/2
            y -= self.altoPantalla/2      
        elif x==0 and y!=0:
            y -= self.altoPantalla/2
        elif x==0 and y ==0:
            if escala_x < escala_y:
                escala = escala_y
            else:
                escala = escala_x
        #self.ancho = self.ancho * escala
        #self.alto = self.alto * escala
        nueva_y = altoPantalla/2 - (self.alto * escala)/2 + y * escala
        nueva_x = anchoPantalla/2 - (self.ancho * escala)/2 + x * escala
        self.rectangulo[1] = self.rectangulo[1] * escala 
        self.rectangulo[0] = self.rectangulo[0] * escala
        self.rectangulo.topleft = (nueva_x,nueva_y)
        pygame.display.get_surface().blit(pygame.transform.scale(self.imagen, (self.ancho * escala, self.alto * escala)), (nueva_x,nueva_y))

    def obtenerImagen(self) -> pygame.image:
        """Devuelve la imagen en el formato reconocido por pygame."""
        return self.imagen
        