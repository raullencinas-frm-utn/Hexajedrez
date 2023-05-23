# Necesario para usar la clase como anotacion de tipo en sus propios miembros.
from __future__ import annotations

import copy
from typing import Optional
from typing import Union
from hexCoord import HexCoord
from hexCasilla import HexCasilla
from piezas import Piezas


class Tablero:
    """
    Una clase sobre el tablero del juego.
    Proporciona metodos para hacer movimientos, generar tableros comunes, movimientos de una coordenada y detectar Jaque y Jaque Mate.
    """

    def __init__(self, colores: str, casillas=None):
        """Constructor del tablero."""
        if casillas is None:
            casillas = dict()
        self.casillas: dict[int, HexCasilla] = casillas
        self.coordenadasACasillas: dict[HexCoord, int] = dict()
        self.piezas = Piezas(colores)
        self.movimientos = self.piezas.movimientos()
        self.turno: int = 0

    def __iter__(self):
        """Regresa un iterador de las coordenadas sobre el mapa."""
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
        """Verifica que la coordenada se encuentra en el mapa."""
        if type(item) is HexCoord:
            return item in self.coordenadasACasillas.keys()
        elif type(item) is int:
            return item in self.casillas.keys()

    @staticmethod
    def generarConRadio(radio: int, colores: str) -> Tablero:
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
        # Coordenadas de cada una de las piezas de acuerdo a la variante de Dave McCooey

        McCooeyPos: dict[str, list[tuple]] = {
            "b_peon": [(-n, -2, n + 2) for n in range(4)] + [(n, -n - 2, 2) for n in range(4)],
            "b_caballo": [(-1, -3, 4), (1, -4, 3)],
            "b_torre": [(-2, -3, 5), (2, -5, 3)],
            "b_alfil": [(0, -3, 3), (0, -4, 4), (0, -5, 5)],
            "b_reina": [(-1, -4, 5)],
            "b_rey": [(1, -5, 4)],

            "n_peon": [(-n, 2+n, -2) for n in range(4)] + [(n, 2, -2-n) for n in range(4)],
            "n_alfil": [(0, 5, -5), (0, 4, -4), (0, 3, -3)],
            "n_reina": [(-1, 5, -4)],
            "n_rey": [(1, 4, -5)],
            "n_torre": [(-2, 5, -3), (2, 3, -5)],
            "n_caballo": [(1, 3, -4), (-1, 4, -3)],
        }

        # Verifica si hay 3 jugadores.
        if colores.endswith("r"):
            # Realiza las posiciones de las piezas para 3 jugadores: blanco, negro y rojo
            McCooeyPos.update({
                "n_peon": [(-2-n, 2, +n) for n in range(4)] + [(-2, 2 + n, -n) for n in range(4)],
                "n_alfil": [(-5, 5, 0), (-4, 4, 0), (-3, 3, 0)],
                "n_reina": [(-4, 5, -1)],
                "n_rey": [(-5, 4, 1)],
                "n_torre": [(-3, 5, -2), (-5, 3, 2)],
                "n_caballo": [(-4, 3, 1), (-3, 4, -1)],

                "r_peon": [(2, +n, -2-n) for n in range(4)] + [(2 + n, -n, -2) for n in range(4)],
                "r_alfil": [(5, 0, -5), (4, 0, -4), (3, 0, -3)],
                "r_reina": [(5, -1, -4)],
                "r_rey": [(4, 1, -5)],
                "r_torre": [(5, -2, -3), (3, 2, -5)],
                "r_caballo": [(3, 1, -4), (4, -1, -3)],
            })

        # Generar un mapa inicial.
        mapaInicial: Tablero = Tablero.generarConRadio(5, colores)

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

                # Si las piezas son del mismo color no se puede mover a ese lugar.
                if self[hexagonoActual] is not None and self[hexagonoActual][0] == coordPiezaInicial[0]:
                    break
                
                # Si el rey se encuentra en jaque tras este movimiento:
                if self.jaqueAlMoverse(coordPiezaInicial[0], posInicial, hexagonoActual):
                    # El peon, el caballo, y el rey solo pueden moverse una celda a la vez.
                    if coordPiezaInicial[2:] in ["rey", "peon", "caballo"]:
                        break
                    # El resto de piezas se mueven hasta los extremos del tablero.
                    else:
                        continue
                    
                # Manejo especial para los movimientos de los peones.
                if coordPiezaInicial.endswith("peon"):
                    diferencia: HexCoord = hexagonoActual - posInicial
                    # Si el peon es blanco:
                    if coordPiezaInicial[0] == "b":
                        # Si es un ataque diagonal pero no hay nadie a quien atacar:
                        if diferencia in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)] and self[hexagonoActual] is None:
                            break
                        
                        if diferencia in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)] and self[hexagonoActual] is not None:
                            movimientosValidos.append(hexagonoActual)
                            break

                        if self[hexagonoActual] is not None:
                            break
                       
                        if diferencia == HexCoord(0, 1, -1) and self[hexagonoActual] is not None:
                            break
                        
                        # Si es un movimiento hacia delante pero hay una pieza en el camino:
                        if diferencia == HexCoord(0, 1, -1) and self[hexagonoActual] is None:
                            if (posInicial.p, posInicial.q, posInicial.r) in ([(-n, -2, n + 2) for n in range(4)] + [(n, -n - 2, 2) for n in range(4)]) and self[hexagonoActual] is None:
                                movimientosValidos.append(hexagonoActual)
                                continue

                    # Si el peon es negro:
                    elif coordPiezaInicial[0] == "n":

                        # Si el modo de juego tiene 3 jugadores:
                        if self.piezas.colores.endswith("r"):

                            # Si es un ataque diagonal pero no hay nadie a quien atacar:
                            if diferencia in [HexCoord(0, -1, 1), HexCoord(1, 0, -1)] and self[hexagonoActual] is None:
                                break
                            
                            if diferencia in [HexCoord(0, -1, 1), HexCoord(1, 0, -1)] and self[hexagonoActual] is not None:
                                movimientosValidos.append(hexagonoActual)
                                break
                            
                            if self[hexagonoActual] is not None:
                                    break

                            if diferencia == HexCoord(1, -1, 0) and self[hexagonoActual] is not None:
                                break
                            # Si es un movimiento hacia delante pero hay una pieza en el camino:
                            if diferencia == HexCoord(1, -1, 0) and self[hexagonoActual] is None:
                                if (posInicial.p, posInicial.q, posInicial.r) in ([(-2-n, 2, +n ) for n in range(4)] + [(-2, 2 +n , -n) for n in range(4)]):
                                    movimientosValidos.append(hexagonoActual)
                                    continue

                        # Si el modo de juego tiene 2 jugadores:
                        else:

                            # Si es un ataque diagonal pero no hay nadie a quien atacar:
                            if diferencia in [HexCoord(1, -1, 0), HexCoord(-1, 0, 1)] and self[hexagonoActual] is None:
                                break
                            
                            if diferencia in [HexCoord(1, -1, 0), HexCoord(-1, 0, 1)] and self[hexagonoActual] is not None:
                                movimientosValidos.append(hexagonoActual)
                                break
                            
                            if self[hexagonoActual] is not None:
                                    break
                                
                            # Si es un movimiento hacia delante pero hay una pieza en el camino:
                            if diferencia == HexCoord(0, -1, 1) and self[hexagonoActual] is not None:
                                break
                            
                            # Si es un movimiento hacia delante pero hay una pieza en el camino:
                            if diferencia == HexCoord(0, -1, 1) and self[hexagonoActual] is None:
                                
                                if (posInicial.p, posInicial.q, posInicial.r) in ([(-n, 2+n, -2 ) for n in range(4)] + [(n, 2 , -2-n) for n in range(4)]):
                                    movimientosValidos.append(hexagonoActual)
                                    continue
                
                    # Si el peon es rojo:
                    elif coordPiezaInicial[0] == "r":

                        # Si es un ataque diagonal pero no hay nadie a quien atacar:
                        if diferencia in [HexCoord(-1, 1, 0), HexCoord(0, -1, 1)] and self[hexagonoActual] is None:
                            break
                        
                        if diferencia in [HexCoord(-1, 1, 0), HexCoord(0, -1, 1)] and self[hexagonoActual] is not None:
                            movimientosValidos.append(hexagonoActual)
                            break

                        if self[hexagonoActual] is not None:
                                    break
                        
                        if diferencia == HexCoord(-1, 0, 1) and self[hexagonoActual] is not None:
                                    break
                        # Si es un movimiento hacia delante pero hay una pieza en el camino:
                        if diferencia == HexCoord(-1, 0, 1) and self[hexagonoActual] is None:
                            if (posInicial.p, posInicial.q, posInicial.r) in ([( 2, +n,-2-n ) for n in range(4)] + [( 2 +n, -n, -2) for n in range(4)]):
                                movimientosValidos.append(hexagonoActual)
                                continue

                # Si el movimiento es valido, se agrega a la lista.
                movimientosValidos.append(hexagonoActual)

                # Si hay una pieza en el hexagono, se detiene.
                if self[hexagonoActual] is not None:
                    break

                # El rey, el peón y el caballo solo pueden moverse a lo largo de sus vectores una vez.
                if coordPiezaInicial[2:] in ["rey", "peon", "caballo"]:
                    break
        
        return movimientosValidos
    
    def casillasPiezasMismoColor(self, color: str) -> list[HexCasilla]:
        """Devuelve todas las casillas que tengan una pieza de un color especifico."""
        celdasValidas: list[HexCasilla] = []
        for casilla in self:
            if casilla.estado is not None and casilla.estado.startswith(color):
                celdasValidas.append(casilla)
        return celdasValidas

    def movimientosPorColor(self, color: str) -> tuple[HexCoord, HexCoord]:
        """Devuelve todos los movimientos de las piezas de un color especifico."""
        for casilla in self.casillasPiezasMismoColor(color):
            for coordenada in self.generarMovimientos(casilla.coordenada):
                if casilla.coordenada != coordenada:
                    yield casilla.coordenada, coordenada

    def moverPieza(self, posInicial: HexCoord, posFinal: HexCoord, desde: str):
        """Realiza el movimiento desde posicion inicial hasta la posicion final."""
        if posInicial == posFinal:
            return
        else:
            self[posFinal] = self[posInicial]
            self[posInicial] = None
            if desde != "":
                self.turno += 1
                piezaMovida = self.__getitem__(posFinal)

                # Si la pieza movida es un peon:
                if piezaMovida[2:] == "peon":
                    # Si el peon es blanco:
                    if (piezaMovida[0] == "b"):
                        if ((posFinal.q) == 5 or (posFinal.r) == -5):
                            self.__setitem__(posFinal, "b_reina")
                    # Si el peon es negro:
                    elif (piezaMovida[0] == "n"):
                        # Si hay 3 jugadores:
                        if (self.piezas.colores.endswith("r")):
                            if ((posFinal.p) == 5 or (posFinal.q) == -5):
                                self.__setitem__(posFinal, "n_reina")
                        # Si hay 2 jugadores:
                        else:
                            if ((posFinal.q) == -5 or (posFinal.r) == 5):
                                self.__setitem__(posFinal, "n_reina")
                    # Si el peon es rojo:
                    else:
                        if ((posFinal.p) == -5 or (posFinal.q) == 5):
                            self.__setitem__(posFinal, "r_reina")
            
    def elReyEstaEnJaque(self, color: str) -> bool:
        """Comprobar si un rey del color especificado está en jaque en este momento."""

        # Debe encontrar la coordenada en la que se encuentra el rey, para verificar los movimientos enemigos.
        coordenadaRey: Optional[HexCoord] = None
        for casilla in self:
            if casilla.estado == f"{color}_rey":
                coordenadaRey = casilla.coordenada

        # Iterar sobre el diccionario de celdas, sobre los valores del par de claves.
        for coordenada, casilla in self.casillas.items():

            # Si no hay nada en esa casilla, no hay necesidad de comprobar si puede amenazar al rey.
            if casilla.estado is None:
                continue

            # Si la pieza es del mismo color que el rey, es seguro que no lo amenaza.
            if casilla.estado[0] == color:
                continue

            # Esta pieza debe ser ahora sin duda una pieza enemiga, así que itera sobre sus "movimientos":
            for orientacion in self.movimientos[casilla.estado]:
                # Convierta la tupla de 3 en un `HexCoord` para aprovechar sus operadores y métodos sobrecargados.
                orientacion: HexCoord = HexCoord(*orientacion)
                hexagonoActual: HexCoord = casilla.coordenada

                while True:

                    # Recorre sobre la linea en direccion a la orientación.
                    hexagonoActual += orientacion

                    # Si la coordenada en la que se encuentra está fuera de los límites se deja de moverse a lo largo de esa línea.
                    if hexagonoActual not in self:
                        break

                    # Si la pieza en la coordenada es del mismo color que la indicada, deja de moverse a lo largo de esta línea.
                    if self[hexagonoActual] is not None and self[hexagonoActual][0] == casilla.estado[0]:
                        break

                    # Manejo especial de las peculiaridades de las piezas de peon
                    if casilla.estado.endswith("peon"):
                        offset: HexCoord = hexagonoActual - casilla.coordenada

                        # Comprobar que el desplazamiento es un ataque, ya que los peones no pueden amenazar a los que se encuentran adelante.
                        if casilla.estado[0] == "b":
                            if offset not in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)]:
                                break
                        elif casilla.estado[0] == "n":
                            if self.piezas.colores.endswith("r"):
                                if offset not in (HexCoord(0, -1, 1), HexCoord(1, 0, -1)):
                                    break
                            else:
                                if offset not in (HexCoord(1, -1, 0), HexCoord(-1, 0, 1)):
                                    break
                        elif casilla.estado[0] == "r":
                            if offset not in (HexCoord(-1, 1, 0), HexCoord(0, -1, 1)):
                                break

                    # La jugada paso todos los jaques, asi que si amenaza al rey, el rey esta en jaque.
                    if hexagonoActual == coordenadaRey:
                        return True

                    # Si esto es cierto, debe ser el caso de que es una pieza enemiga distinta del rey, por lo que no se puede recorrer a lo largo de este vector.
                    elif self[hexagonoActual] is not None:
                        break

                    #Rey, Peón y Caballo sólo pueden moverse a lo largo de sus movimientos una vez.
                    #Se ejecutará en el primer ciclo de cualquier vector, deteniendo el movimientto para ellos.
                    elif casilla.estado[2:] in ["rey", "peon", "caballo"]:
                        break

        # El rey no está en jaque.
        return False
    
    def elReyEstaEnJaqueMate(self, color: str) -> bool:
        """Revisa si un rey del color especificado se encuentra en situacion de Jaque Mate."""
        # Si el rey se encuentra en Jaque:
        if self.elReyEstaEnJaque(color):
            # Si ninguna pieza puede moverse significa que se encuentra en Jaque Mate:
            if all(len(self.generarMovimientos(celda.coordenada)) == 1 for celda in self.casillasPiezasMismoColor(color)):
                return True
        return False

    def jaqueAlMoverse(self, color: str, posInicial: HexCoord, posFinal: HexCoord) -> bool:
        """Revisa si el rey de un especifico color se encuentra en Jaque tras un movimiento."""
        respaldo: Optional[str] = self[posFinal]

        self.moverPieza(posInicial, posFinal,"")
        estadoDeJaque: bool = self.elReyEstaEnJaque(color)
        self.moverPieza(posFinal, posInicial,"")

        self[posFinal] = respaldo
        return estadoDeJaque