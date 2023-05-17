import pygame


class Boton:
    def __init__(self, x, y, imagen, escala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(
            imagen, (int(ancho * escala), int(alto * escala))
        )
        self.rectangulo = self.imagen.get_rect()
        self.rectangulo.topleft = (x, y)
        self.seleccionado = False

    def dibujar(self, pantalla):
        accion = False
        # obtenemos posicion de mouse
        pos = pygame.mouse.get_pos()

        # check mouseover and seleccionado conditions
        if self.rectangulo.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.seleccionado == False:
                self.seleccionado = True
                accion = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.seleccionado = False

        # draw button on screen
        pantalla.blit(self.imagen, (self.rectangulo.x, self.rectangulo.y))

        return accion
