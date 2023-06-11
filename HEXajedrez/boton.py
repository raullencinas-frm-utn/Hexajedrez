import pygame
from sonido import Sonido

class Boton:
    def __init__(self, x, y, imagen, escala):

        """Constructor de un boton."""

        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(
            imagen, (int(ancho * escala), int(alto * escala)))
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.topleft = (x, y)
        self.seleccionado = False

    def dibujar(self, posicion, sonido):

        """Dibujar el boton en pantalla."""

        accion = False
    
        # Obtenemos posicion del mouse
    
        pos = pygame.mouse.get_pos()
        # Revisar que el mouse se encuentre encima del boton y haga click

        if self.rectangulo.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.seleccionado == False:
                if sonido:
                    Sonido.sonidoBoton()
                self.seleccionado = True
                accion = True

        # Se suelta el boton del mouse
        if pygame.mouse.get_pressed()[0] == 0:
            self.seleccionado = False

        # Si se indica la posicion del boton como "Centrado" se calcula su posicion en el centro de la pantalla.

        if posicion == "Centrado":
            anchoPantalla, altoPantalla = pygame.display.get_window_size()
            self.rectangulo.x = (anchoPantalla / 2) - \
                (self.imagen.get_width() / 2)
        
        transparencia = 180 if self.seleccionado else 255
        self.imagen.set_alpha(transparencia)

        # Dibujar boton en pantalla
        pygame.display.get_surface().blit(self.imagen, (self.rectangulo.x, self.rectangulo.y))

        return accion
