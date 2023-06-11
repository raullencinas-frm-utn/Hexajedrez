import pygame

class Sonido:
    """Una clase para poder reproducir sonidos dependiendo de si el usuario los ha desactivado o no."""

    volumen = True
   
    @staticmethod
    def init():
        pygame.init()

    @staticmethod
    def sonidoBoton():
        sonido = pygame.mixer.Sound("sonido/Boton_Sound.ogg")
        sonido.set_volume(Sonido.volumen)
        sonido.play()

    @staticmethod
    def sonidoTomarPieza(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/Movimiento_Sound.ogg")
            Sonido.play()

    @staticmethod
    def sonidoSoltarPieza(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/Movimiento_soltar.ogg")
            Sonido.play()
    
    @staticmethod
    def sonidoIniciarJuego(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/board-start.ogg")
            Sonido.play()

    
