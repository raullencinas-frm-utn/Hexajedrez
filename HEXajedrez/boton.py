import pygame


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

    def dibujar(self, posicion):
        """Dibujar el boton en pantalla."""
        accion = False
        # obtenemos posicion de mouse
        pos = pygame.mouse.get_pos()

        # Revisar condicionales del mouse que se encuentre encima del boton y haga click
        if self.rectangulo.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.seleccionado == False:
                self.seleccionado = True
                accion = True

        # Se suelta el boton del mouse
        if pygame.mouse.get_pressed()[0] == 0:
            self.seleccionado = False

        # Dibujar boton en pantalla
        if posicion == "Centrado":
            anchoPantalla, altoPantalla = pygame.display.get_window_size()
            self.rectangulo.x = (anchoPantalla / 2) - \
                (self.imagen.get_width() / 2)
        
        pygame.display.get_surface().blit(self.imagen, (self.rectangulo.x, self.rectangulo.y))

        return accion
