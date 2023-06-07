import pygame

class Sonido:
   
    """Una clase para poder reproducir sonidos dependiendo de si el usuario los ha desactivado o no."""
   
    @staticmethod
    def init():
        pygame.init()
    
    @staticmethod
    def sonidoBoton():
        Sonido = pygame.mixer.Sound("sonido/Boton_Sound.mp3")
        Sonido.play()

    @staticmethod
    def sonidoTomarPieza(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/Movimiento_Sound.ogg")
            Sonido.play()

    @staticmethod
    def sonidoSoltarPieza(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/Movimiento_soltar.mp3")
            Sonido.play()
    
    @staticmethod
    def sonidoIniciarJuego(son: bool):
        if son:
            Sonido = pygame.mixer.Sound("sonido/board-start.mp3")
            Sonido.play()

    
