import os
import pygame
import random

class Musica:
    """Una clase que permite reproducir una de varias canciones aleatoriamente."""
    listaCanciones = []
    
    def __init__(self, carpeta :str ):

        # Direccion de la carpeta que contiene las canciones.
        self.carpetaCanciones = carpeta  

        # Archivos de la carpeta de las canciones.
        for archivo in os.listdir(self.carpetaCanciones): 

            # Si termina en .mp3, se agrega a la lista de canciones.
            if archivo.endswith(".mp3"):
                rutaCancion = os.path.join(self.carpetaCanciones, archivo)
                self.listaCanciones.append(rutaCancion)
    
    def iniciar(self, reproducir_musica:bool):
        """Se reproduce la musica."""

        if reproducir_musica:

            # Reproduce al azar una cancion de la lista.
            pygame.mixer.music.load(random.choice(self.listaCanciones))
            pygame.mixer.music.play(-1)    