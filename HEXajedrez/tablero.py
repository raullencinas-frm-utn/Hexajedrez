from __future__ import annotations  # Necessary to use the class as a type annotation in its own members.

import copy
from typing import Optional  # For T | None annotations.
from typing import Union
from hexCoord import  HexCoord
from hexCasilla import HexCasilla

class Tablero:
    """
    Una clase sobre el tablero del juego.
    Proporciona métodos para hacer movimientos, generar tableros comunes, movimientos de una coordenada y detectar Jaque y Jaque Mate.
    """
    def __init__(self,colores: str, casillas=None):
            if casillas is None:
                casillas = dict()
            self.casillas: dict[int, HexCasilla] = casillas
            self.coordenadasACasillas: dict[HexCoord, int] = dict()
        
    def __iter__(self):
        """Regrese un iterador de las coordenadas sobre el mapa."""
        return iter(self.casillas.values())
            
    def __getitem__(self, item: Union[int, HexCoord]) -> Optional[str]:
        """Busca la coordenada en un mapa y retorna el estado de una celda."""
        if type(item) is HexCoord:
            return self.casillas[self.coordenadasACasillas[item]].estado
        elif type(item) is int:
            return self.casillas[item].estado

    def __setitem__(self, clave: Union[int, HexCoord], valor: Optional[str]):
        """Ingresa el estado de una celda en un mapa a partir de una coordenada."""
        if type(clave) is HexCoord:
            self.casillas[self.coordenadasACasillas[clave]].estado = valor
        elif type(clave) is int:
            self.casillas[clave].estado = valor

    def __contains__(self, item: HexCoord) -> bool:
        """
        Verifica que la coordenada esta en el mapa.
        """
        if type(item) is HexCoord:
            return item in self.coordenadasACasillas.keys()
        elif type(item) is int:
            return item in self.casillas.keys()

    @staticmethod
    def aPartirDeRadio(radio: int,colores:str) -> Tablero:
        """
        Genera un mapa de haxagonos de un cierto radio.

        """
        tablero = Tablero(colores)
        i = 0
        for p in range(-radio, radio + 1):
            for q in range(-radio, radio + 1):
                for r in range(-radio, radio + 1):
                    if p + q + r == 0:
                        coord = HexCoord(p, q, r)
                        tablero.coordenadasACasillas[copy.deepcopy(coord)] = i
                        tablero.casillas[i] = HexCasilla(coord)
                        i += 1
        return tablero

    @staticmethod
    def aPartirDeGlinski(colores: str) -> Tablero:
        """Generar un mapa de hexagonos de una variante Glinski."""

        # Generar un mapa inicial.
        mapaInicial: Tablero = Tablero.aPartirDeRadio(5,colores)

        return mapaInicial
