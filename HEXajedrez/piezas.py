import pygame 

class Piezas:
    
    nombres = ("peon","torre","caballo","alfil","rey","reina")

    def __init__(self,colores :str):
        self.colores = colores
    #se devuelve una un dict[str, pygame.Surface] de las piezas de los colores que entran por parametro
    def piezasImagenes(self,colores: str) -> dict[str, pygame.Surface]:
        return {
            nombresDePiezas: pygame.transform.scale(
                pygame.image.load(f"img/{nombresDePiezas}.png").convert_alpha(),
                (60, 60)
            )
            for nombresDePiezas in [f"{color}_{nombre}" for color in self.colores for nombre in self.nombres]
    
            }    
        
            
