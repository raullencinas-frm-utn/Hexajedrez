import os
import pygame
import random

class Musica:
    """Una clase que permite reproducir una de varias canciones aleatoriamente."""
    listaCanciones = []
    
    def __init__(self, carpeta :str ):
        self.carpetaCanciones = carpeta  # Direccion de la carpeta que contiene las canciones.
        for archivo in os.listdir(self.carpetaCanciones): # Archivo de la cancion.
            if archivo.endswith(".mp3"):
                rutaCancion = os.path.join(self.carpetaCanciones, archivo)
                self.listaCanciones.append(rutaCancion)
    
    def iniciar(self, reproducir_musica:bool):
        if reproducir_musica:
            pygame.mixer.music.load(random.choice(self.listaCanciones))
            pygame.mixer.music.play(-1)    