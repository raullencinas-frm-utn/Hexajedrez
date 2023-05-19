from __future__ import annotations  # Necesario para usar la clase como anotacion de tipo en sus propios miembros.

import copy
from typing import Optional  
from typing import Union
from hexCoord import  HexCoord
from hexCasilla import HexCasilla
from piezas import Piezas

class Tablero:
    """
    Una clase sobre el tablero del juego.
    Proporciona metodos para hacer movimientos, generar tableros comunes, movimientos de una coordenada y detectar Jaque y Jaque Mate.
    """
    def __init__(self,colores: str, casillas=None):
        """Constructor del tablero."""
        if casillas is None:
            casillas = dict()
        self.casillas: dict[int, HexCasilla] = casillas
        self.coordenadasACasillas: dict[HexCoord, int] = dict()
        self.piezas = Piezas(colores)
        self.movimientos = self.piezas.movimientos()

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
        Verifica que la coordenada se encuentra en el mapa.
        """
        if type(item) is HexCoord:
            return item in self.coordenadasACasillas.keys()
        elif type(item) is int:
            return item in self.casillas.keys()

    @staticmethod
    def generarConRadio(radio: int,colores:str) -> Tablero:
        """Genera un mapa de hexagonos de un cierto radio."""
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
    def generarMcCooey(colores: str) -> Tablero:
        """Generar un mapa de hexagonos de una variante Dave McCooey."""
        #coordenadas de cada una de las piezas de acuerdo a la variante de Dave McCooey
        
        McCooeyPos: dict[str, list[tuple]] = {
                "b_peon": [(-n, -2, n + 2) for n in range(4)] + [(n, -n - 2, 2) for n in range(4)],
                "b_caballo": [(-1, -3, 4), (1, -4, 3)],
                "b_torre": [(-2, -3, 5), (2, -5, 3)],
                "b_alfil": [(0, -3, 3), (0, -4, 4), (0, -5, 5)],
                "b_reina": [(-1, -4, 5)],
                "b_rey": [(1, -5, 4)]
        }

        # Verifica si hay 3 jugadores.
        if colores.endswith("r"):
            # Realiza las posiciones de las piezas para 3 jugadores: blanco, negro y rojo
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
            # Realiza las posiciones de las piezas para 2 jugadores: blanco y negro
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
        mapaInicial: Tablero = Tablero.generarConRadio(5,colores)
        
        for pieza, listaPosiciones in McCooeyPos.items():
            for posicion in listaPosiciones:
                mapaInicial[HexCoord(*posicion)] = pieza

        return mapaInicial

    def generarMovimientos(self, posInicial: HexCoord) -> list[HexCoord]:
        """
        Genera todos los posibles movimientos a partir de un hexagono inicial
        Comprueba a donde puede moverse hasta que deba detenerse.
        """
        coordPiezaInicial: Optional[str] = self[posInicial]

        # Si no se encuentra nada en el hexagono, se detiene.
        if coordPiezaInicial is None:
            return []

        # Una pieza siempre puede moverse al hexagono inicial.
        movimientosValidos: list[HexCoord] = [posInicial]

        for orientacion in self.movimientos[coordPiezaInicial]:
            # Convierte la tupla de 3 valores en una coordenada axial / hexagonal.
            orientacion: HexCoord = HexCoord(*orientacion)
            hexagonoActual: HexCoord = posInicial

            while True:
                # Viaja 1 hexagono en la direccion indicada.
                hexagonoActual += orientacion

                # Si la coordenada esta fuera del tablero, se detiene.
                if hexagonoActual not in self:
                    break

                # Si el movimiento es valido, se agrega a la lista.
                movimientosValidos.append(hexagonoActual)

                # Si hay una pieza en el hexagono, se detiene.
                if self[hexagonoActual] is not None:
                    break

        return movimientosValidos

    def moverPieza(self, posInicial: HexCoord, posFinal: HexCoord,desde : str):
        """Realiza el movimiento desde posicion inicial hasta la posicion final."""
        if posInicial == posFinal:
            return
        self[posFinal] = self[posInicial]
        self[posInicial] = None
