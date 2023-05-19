import pygame 

class Piezas:
    
    nombres = ("peon","torre","caballo","alfil","rey","reina")

    def __init__(self,colores :str):
        """Constructor de una pieza."""
        self.colores = colores
        
    def piezasImagenes(self,colores: str) -> dict[str, pygame.Surface]:
        """Devuelve un diccionario con las imagenes de las piezas del color ingresado."""
        return {
            nombresDePiezas: pygame.transform.scale(
                pygame.image.load(f"img/{nombresDePiezas}.png").convert_alpha(),
                (60, 60)
            )
            for nombresDePiezas in [f"{color}_{nombre}" for color in self.colores for nombre in self.nombres]
            }    
        
    def movimientos(self) -> dict[str, list]:
        """Devuelve un diccionario con los movimientos de cada una de las piezas."""
        movimientos = {
                **dict.fromkeys([f"{color}_{nombre}" for color in self.colores for nombre in self.nombres], [
                    (0, 1, -1), (0, -1, 1),
                    (1, 0, -1), (-1, 0, 1),
                    (1, -1, 0), (-1, 1, 0),
                    (2, -1, -1), (-2, 1, 1),
                    (-1, 2, -1), (1, -2, 1),
                    (-1, -1, 2), (1, 1, -2)
                ])
            }
        
        return movimientos

    