import pygame
from sonido import Sonido
import time

class Boton:
    def __init__(self, x, y, imagen):
        """Constructor de un boton."""
        self.anchoPantalla, self.altoPantalla = pygame.display.get_surface().get_size()
        self.ancho = imagen.get_width()
        self.alto = imagen.get_height()
        self.imagen = imagen
        self.rectangulo = self.imagen.get_rect()
        self.x = x
        self.y = y
        self.rectangulo.topleft = (x, y)
        self.seleccionado = False

    def dibujar(self) -> bool:
        """Se dibuja el boton y devuelve un valor verdadero si se presiona."""
        x= self.x
        y= self.y
        anchoPantalla, altoPantalla = pygame.display.get_surface().get_size()
        
        # Dimension de pantalla
        escala_x = anchoPantalla / self.anchoPantalla
        escala_y = altoPantalla / self.altoPantalla

        if escala_x > escala_y:
            escala = escala_y
        else:
            escala = escala_x

        if x != 0: 
            x -= self.anchoPantalla/2
        y -= self.altoPantalla/2
        
        # Redimension de pantalla. 
        nueva_y = altoPantalla/2 - (self.alto * escala)/2 + y * escala
        nueva_x = anchoPantalla/2 - (self.ancho * escala)/2 + x * escala
    
        rectangulo = pygame.Rect(nueva_x,nueva_y,(self.ancho * escala),(self.alto * escala))

        
        """Dibujar el boton en pantalla."""
        accion = False
        # Obtenemos posicion del mouse
        pos = pygame.mouse.get_pos()
        
        # Revisar que el mouse se encuentre encima del boton y haga click

        if rectangulo.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.seleccionado:
                self.seleccionado = True
                Sonido.sonidoBoton()
            
        transparencia = 150 if self.seleccionado else 255
        self.imagen.set_alpha(transparencia)

        # Se suelta el boton del mouse
        if pygame.mouse.get_pressed()[0] == 0:
            if self.seleccionado:
                accion = True
            self.seleccionado = False

        # Dibujar boton en pantalla
        pygame.display.get_surface().blit(pygame.transform.scale(self.imagen, (self.ancho * escala, self.alto * escala)), (rectangulo.x, rectangulo.y))

        return accion
