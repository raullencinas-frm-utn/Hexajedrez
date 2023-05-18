from __future__ import annotations  # Necessary to use the class as a type annotation in its own members.

import copy
from typing import Optional  # For T | None annotations.
from typing import Union
from hexCoord import  HexCoord
from hexCasilla import HexCasilla
from piezas import Piezas

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
            self.piezas = Piezas(colores)
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
        #coordenadas de cada una de las piezas segun De Dave McCooey
        
        McCooeyPos: dict[str, list[tuple]] = {
                "b_peon": [(-n, -2, n + 2) for n in range(4)] + [(n, -n - 2, 2) for n in range(4)],
                "b_caballo": [(-1, -3, 4), (1, -4, 3)],
                "b_torre": [(-2, -3, 5), (2, -5, 3)],
                "b_alfil": [(0, -3, 3), (0, -4, 4), (0, -5, 5)],
                "b_reina": [(-1, -4, 5)],
                "b_rey": [(1, -5, 4)]
        }
        #chequea si la variable colores termina con r
        if colores.endswith("r"):
            #en el caso que sea r da la posicion para 3 jugadores, blanco negro y rojo
            McCooeyPos.update({
                "n_peon": [(-2-n, 2, +n ) for n in range(4)] + [(-2, 2 +n , -n) for n in range(4)],
                "n_alfil": [(-5, 5, 0), (-4, 4, 0), (-3, 3, 0)],
                "n_reina": [(-4, 5, -1)],
                "n_rey": [( -5, 4, 1)],
                "n_torre": [( -3, 5, -2), ( -5, 3, 2)],
                "n_caballo": [(-4, 3, 1), (-3, 4, -1)],
                
                "r_peon": [( 2, +n,-2-n ) for n in range(4)] + [( 2 +n, -n, -2) for n in range(4)],
                "r_alfil": [(5, 0, -5), ( 4, 0, -4), ( 3, 0, -3)],
                "r_reina": [( 5, -1, -4)],
                "r_rey": [(  4, 1, -5)],
                "r_torre": [(  5, -2, -3), (  3, 2, -5)],
                "r_caballo": [( 3, 1, -4), ( 4, -1, -3)],
            })
        else:
            #en el caso que no termine en r da solo para 2 jugadores blanco y negro
            McCooeyPos.update({
                "b_peon": [(-n, -2, n + 2) for n in range(4)] + [(n, -n - 2, 2) for n in range(4)],
                "b_caballo": [(-1, -3, 4), (1, -4, 3)],
                "b_torre": [(-2, -3, 5), (2, -5, 3)],
                "b_alfil": [(0, -3, 3), (0, -4, 4), (0, -5, 5)],
                "b_reina": [(-1, -4, 5)],
                "b_rey": [(1, -5, 4)],

                "n_peon": [(-n, 2+n, -2 ) for n in range(4)] + [(n, 2 , -2-n) for n in range(4)],
                "n_alfil": [(0,5,-5), (0, 4, -4), (0, 3, -3)],
                "n_reina": [(-1, 5, -4)],
                "n_rey": [( 1, 4, -5)],
                "n_torre": [( -2, 5, -3), ( 2, 3, -5)],
                "n_caballo": [(1, 3, -4), (-1, 4, -3)],
                
            })

        # Generar un mapa inicial.
        mapaInicial: Tablero = Tablero.aPartirDeRadio(5,colores)
        
        for pieza, listaPosiciones in McCooeyPos.items():
            for posicion in listaPosiciones:
                mapaInicial[HexCoord(*posicion)] = pieza

        return mapaInicial

