# Necesario para usar la clase como anotacion de tipo en sus propios miembros.
from __future__ import annotations

import copy
import string
import pygame
from typing import Optional
from typing import Union
from hexCoord import HexCoord
from hexCelda import HexCelda
from piezas import Piezas
from boton import Boton
from imagen import Imagen


class Tablero:
    """
    Una clase sobre el tablero del juego.
    Proporciona metodos para hacer movimientos, generar tableros comunes, movimientos de una coordenada y detectar Jaque y Jaque Mate.
    """

    def __init__(self, colores: str, celdas=None):
        """Constructor del tablero."""
        if celdas is None:
            celdas = dict()
        self.celdas: dict[int, HexCelda] = celdas
        self.coordenadasACeldas: dict[HexCoord, int] = dict()
        self.piezas = Piezas(colores)
        self.movimientos = self.piezas.movimientos()
        self.turno: int = 0

    def __iter__(self):
        """Regresa un iterador de las coordenadas sobre el mapa."""
        return iter(self.celdas.values())

    def __getitem__(self, item: Union[int, HexCoord]) -> Optional[str]:
        """Busca la coordenada en un mapa y retorna el estado de una celda."""
        if type(item) is HexCoord:
            return self.celdas[self.coordenadasACeldas[item]].estado
        elif type(item) is int:
            return self.celdas[item].estado

    def __setitem__(self, clave: Union[int, HexCoord], valor: Optional[str]):
        """Ingresa el estado de una celda en un mapa a partir de una coordenada."""
        if type(clave) is HexCoord:
            self.celdas[self.coordenadasACeldas[clave]].estado = valor
        elif type(clave) is int:
            self.celdas[clave].estado = valor

    def __contains__(self, item: HexCoord) -> bool:
        """Verifica que la coordenada se encuentra en el mapa."""
        if type(item) is HexCoord:
            return item in self.coordenadasACeldas.keys()
        elif type(item) is int:
            return item in self.celdas.keys()

    def __str__(self) -> str:
        FEN_dict = {
            None: "xx",

            "b_peon": "Pb",
            "n_peon": "Pn",
            "r_peon": "Pr",

            "b_torre": "Tb",
            "n_torre": "Tn",
            "r_torre": "Tr",

            "b_rey": "Rb",
            "n_rey": "Rn",
            "r_rey": "Rr",

            "b_alfil": "Ab",
            "n_alfil": "An",
            "r_alfil": "Ar",

            "b_dama": "Db",
            "n_dama": "Dn",
            "r_dama": "Dr",

            "b_caballo": "Cb",
            "n_caballo": "Cn",
            "r_caballo": "Cr"
        }

        hash_str = ""
        for i in range(91):
            hash_str += FEN_dict[self[i]]
        return hash_str

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
                        tablero.coordenadasACeldas[copy.deepcopy(coord)] = i
                        tablero.celdas[i] = HexCelda(coord)
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
            "b_dama": [(-1, -4, 5)],
            "b_rey": [(1, -5, 4)],

            "n_peon": [(-n, 2+n, -2) for n in range(4)] + [(n, 2, -2-n) for n in range(4)],
            "n_alfil": [(0, 5, -5), (0, 4, -4), (0, 3, -3)],
            "n_dama": [(-1, 5, -4)],
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
                "n_dama": [(-4, 5, -1)],
                "n_rey": [(-5, 4, 1)],
                "n_torre": [(-3, 5, -2), (-5, 3, 2)],
                "n_caballo": [(-4, 3, 1), (-3, 4, -1)],

                "r_peon": [(2, +n, -2-n) for n in range(4)] + [(2 + n, -n, -2) for n in range(4)],
                "r_alfil": [(5, 0, -5), (4, 0, -4), (3, 0, -3)],
                "r_dama": [(5, -1, -4)],
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

    def encontrarCoordenadaReal(hexagono: HexCoord) -> str:
        """Retorna un texto con las coordenadas del hexagono en formato letra y número."""
        # Realiza una corrección en las coordenadas en donde desplaza las coordenadas verticales según la letra.
        desplazamiento = abs(hexagono.p) if hexagono.p < 0 else 0
        # Convierte la coordenada p en una letra de la A a la K, y convierte la coordenada q en un numero del 1 al 11.
        return (string.ascii_uppercase[5+hexagono.p]+str(6+hexagono.q-desplazamiento))

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
                    if coordPiezaInicial[2:] in ["rey", "peon", "caballo"] or self[hexagonoActual] is not None:
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
                        
                        # Si es un movimiento hacia delante pero hay una pieza en el camino:
                        if diferencia in [HexCoord(0, 1, -1), HexCoord(0, 2, -2)] and self[hexagonoActual] is not None:
                            break
                        
                        # Si se encuentra en la posicion inicial de un peon, se permite mover una celda adicional:
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
                            
                            # Si es un movimiento hacia delante pero hay una pieza en el camino:
                            if diferencia in [HexCoord(1, -1, 0), HexCoord(2, -2, 0)] and self[hexagonoActual] is not None:
                                break
                            
                            # Si se encuentra en la posicion inicial de un peon, se permite mover una celda adicional:
                            if diferencia == HexCoord(1, -1, 0) and self[hexagonoActual] is None:
                                if (posInicial.p, posInicial.q, posInicial.r) in ([(-2-n, 2, +n ) for n in range(4)] + [(-2, 2 +n , -n) for n in range(4)]):
                                    movimientosValidos.append(hexagonoActual)
                                    continue

                        # Si el modo de juego tiene 2 jugadores:
                        else:

                            # Si es un ataque diagonal pero no hay nadie a quien atacar:
                            if diferencia in [HexCoord(1, -1, 0), HexCoord(-1, 0, 1)] and self[hexagonoActual] is None:
                                break
                                
                            # Si es un movimiento hacia delante pero hay una pieza en el camino:
                            if diferencia in [HexCoord(0, -1, 1), HexCoord(0, -2, 2)] and self[hexagonoActual] is not None:
                                break
                            
                            # Si se encuentra en la posicion inicial de un peon, se permite mover una celda adicional:
                            if diferencia == HexCoord(0, -1, 1) and self[hexagonoActual] is None:
                                if (posInicial.p, posInicial.q, posInicial.r) in ([(-n, 2+n, -2 ) for n in range(4)] + [(n, 2 , -2-n) for n in range(4)]):
                                    movimientosValidos.append(hexagonoActual)
                                    continue
                
                    # Si el peon es rojo:
                    else:

                        # Si es un ataque diagonal pero no hay nadie a quien atacar:
                        if diferencia in [HexCoord(-1, 1, 0), HexCoord(0, -1, 1)] and self[hexagonoActual] is None:
                            break
                        
                        # Si es un movimiento hacia delante pero hay una pieza en el camino:
                        if diferencia in [HexCoord(-1, 0, 1), HexCoord(-2, 0, 2)] and self[hexagonoActual] is not None:
                                    break
                        
                        # Si se encuentra en la posicion inicial de un peon, se permite mover una celda adicional:
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
    
    def celdasPiezasMismoColor(self, color: str) -> list[HexCelda]:
        """Devuelve todas las celdas que tengan una pieza de un color especifico."""
        celdasValidas: list[HexCelda] = []
        for celda in self:
            if celda.estado is not None and celda.estado.startswith(color):
                celdasValidas.append(celda)
        return celdasValidas

    def movimientosPorColor(self, color: str) -> tuple[HexCoord, HexCoord]:
        """Devuelve todos los movimientos de las piezas de un color especifico."""
        for celda in self.celdasPiezasMismoColor(color):
            for coordenada in self.generarMovimientos(celda.coordenada):
                if celda.coordenada != coordenada:
                    yield celda.coordenada, coordenada

    def dibujarMenuPromocion(self, color: str) -> str:
        """Dibuja el menú de promoción y devuelve la pieza seleccionada."""
        PANTALLA = pygame.display.get_surface()
        fuente = pygame.font.SysFont("arialblack", 25)

        imagenDama = Imagen(f"img/{color}_dama.png")
        imagenAlfil = Imagen(f"img/{color}_alfil.png")
        imagenTorre = Imagen(f"img/{color}_torre.png")
        imagenCaballo = Imagen(f"img/{color}_caballo.png")

        # Se crean los botones.
        botonDama = Boton(180, 350, imagenDama.obtenerImagen())
        botonAlfil = Boton(280, 350, imagenAlfil.obtenerImagen())
        botonTorre = Boton(380, 350, imagenTorre.obtenerImagen())
        botonCaballo = Boton(480, 350, imagenCaballo.obtenerImagen())

        selected_piece = None
        ejecucion = True
        while ejecucion:
            pygame.draw.rect(PANTALLA, (0, 0, 0), (150, 280, 400, 150))
            text = fuente.render("¡Selecciona pieza de promocion de peon!", True, (255, 255, 255))
            PANTALLA.blit(text, (180, 310))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecucion = False
                    pygame.quit()
                    exit()

            if botonDama.dibujar():
                selected_piece = "dama"
                ejecucion = False
            elif botonAlfil.dibujar():
                selected_piece = "alfil"
                ejecucion = False
            elif botonTorre.dibujar():
                selected_piece = "torre"
                ejecucion = False
            elif botonCaballo.dibujar():
                selected_piece = "caballo"
                ejecucion = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ejecucion = False
                    pygame.quit()
                    exit()

            pygame.display.flip()

        return f"{color}_{selected_piece}"
    
    def moverPieza(self, posInicial: HexCoord, posFinal: HexCoord, desde: str) -> str:
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
                            self.__setitem__(posFinal, self.dibujarMenuPromocion("b"))
                    # Si el peon es negro:
                    elif (piezaMovida[0] == "n"):
                        # Si hay 3 jugadores:
                        if (self.piezas.colores.endswith("r")):
                            if ((posFinal.p) == 5 or (posFinal.q) == -5):
                                self.__setitem__(posFinal, "n_dama" if desde=="Bot" else self.dibujarMenuPromocion("n"))
                        # Si hay 2 jugadores:
                        else:
                            if ((posFinal.q) == -5 or (posFinal.r) == 5):
                                self.__setitem__(posFinal, "n_dama" if desde=="Bot" else self.dibujarMenuPromocion("n"))
                    # Si el peon es rojo:
                    else:
                        if ((posFinal.p) == -5 or (posFinal.r) == 5):
                            self.__setitem__(posFinal, "r_dama" if desde=="Bot" else self.dibujarMenuPromocion("r"))
                colorPieza = "blanco" if piezaMovida[0]=="b" else "negro" if piezaMovida[0]=="n" else "rojo"
                if piezaMovida[2:].endswith("a"):
                    colorPieza = colorPieza[:-1]+"a"
                return(piezaMovida[2:]+" "+colorPieza+" "+Tablero.encontrarCoordenadaReal(posInicial)+" a "+Tablero.encontrarCoordenadaReal(posFinal))

    def elReyExiste(self, color: str) -> bool:
        """Comprobar si un rey del color especificado existe."""
        return f"R{color}" in self.__str__()

    def contarReyes(self) -> int:
        """Contar la cantidad de reyes en juego."""
        return self.__str__().count("R")

    def elReyEstaEnJaque(self, color: str) -> Optional(HexCoord):
        """Comprobar si un rey del color especificado está en jaque en este momento."""

        # Debe encontrar la coordenada en la que se encuentra el rey, para verificar los movimientos enemigos.
        coordenadaRey: Optional[HexCoord] = None
        for celda in self:
            if celda.estado == f"{color}_rey":
                coordenadaRey = celda.coordenada

        # Iterar sobre el diccionario de celdas, sobre los valores del par de claves.
        for coordenada, celda in self.celdas.items():

            # Si no hay nada en esa celda, no hay necesidad de comprobar si puede amenazar al rey.
            if celda.estado is None:
                continue

            # Si la pieza es del mismo color que el rey, es seguro que no lo amenaza.
            if celda.estado[0] == color:
                continue

            # Si esta pieza no tiene rey, no es una amenaza.
            if not self.elReyExiste(celda.estado[0]):
                continue

            # Esta pieza debe ser ahora sin duda una pieza enemiga, así que itera sobre sus "movimientos":
            for orientacion in self.movimientos[celda.estado]:
                # Convierta la tupla de 3 en un `HexCoord` para aprovechar sus operadores y métodos sobrecargados.
                orientacion: HexCoord = HexCoord(*orientacion)
                hexagonoActual: HexCoord = celda.coordenada

                while True:

                    # Recorre sobre la linea en direccion a la orientación.
                    hexagonoActual += orientacion

                    # Si la coordenada en la que se encuentra está fuera de los límites se deja de moverse a lo largo de esa línea.
                    if hexagonoActual not in self:
                        break

                    # Si la pieza en la coordenada es del mismo color que la indicada, deja de moverse a lo largo de esta línea.
                    if self[hexagonoActual] is not None and self[hexagonoActual][0] == celda.estado[0]:
                        break

                    # Manejo especial de las peculiaridades de las piezas de peon
                    if celda.estado.endswith("peon"):
                        offset: HexCoord = hexagonoActual - celda.coordenada

                        # Comprobar que el desplazamiento es un ataque, ya que los peones no pueden amenazar a los que se encuentran adelante.
                        if celda.estado[0] == "b":
                            if offset not in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)]:
                                break
                        elif celda.estado[0] == "n":
                            if self.piezas.colores.endswith("r"):
                                if offset not in (HexCoord(0, -1, 1), HexCoord(1, 0, -1)):
                                    break
                            else:
                                if offset not in (HexCoord(1, -1, 0), HexCoord(-1, 0, 1)):
                                    break
                        else:
                            if offset not in (HexCoord(-1, 1, 0), HexCoord(0, -1, 1)):
                                break

                    # La jugada paso todos los jaques, asi que si amenaza al rey, el rey esta en jaque.
                    if hexagonoActual == coordenadaRey:
                        return celda.coordenada

                    # Si esto es cierto, debe ser el caso de que es una pieza enemiga distinta del rey, por lo que no se puede recorrer a lo largo de este vector.
                    elif self[hexagonoActual] is not None:
                        break

                    #Rey, Peón y Caballo sólo pueden moverse a lo largo de sus movimientos una vez.
                    #Se ejecutará en el primer ciclo de cualquier vector, deteniendo el movimientto para ellos.
                    elif celda.estado[2:] in ["rey", "peon", "caballo"]:
                        break

        # El rey no está en jaque.
        return None

    def elReyEstaEnJaqueMate(self, color: str) -> bool:
        """Revisa si un rey del color especificado se encuentra en situacion de Jaque Mate."""
        # Si el rey se encuentra en Jaque:
        if self.elReyEstaEnJaque(color)!=None:
            # Si ninguna pieza puede moverse significa que se encuentra en Jaque Mate:
            if self.elReyEstaAhogado(color):
                return True
        return False
    
    def elReyEstaAhogado(self, color: str) -> bool:
        """Revisa si un rey del color especificado se encuentra en situacion de Rey Ahogado."""
        # Si ninguna pieza puede moverse significa que se encuentra ahogado:
        if all(len(self.generarMovimientos(celda.coordenada)) == 1 for celda in self.celdasPiezasMismoColor(color)):
            return True
        return False

    def jaqueAlMoverse(self, color: str, posInicial: HexCoord, posFinal: HexCoord) -> bool:
        """Revisa si el rey de un especifico color se encuentra en Jaque tras un movimiento."""
        respaldo: Optional[str] = self[posFinal]

        self.moverPieza(posInicial, posFinal,"")
        estadoDeJaque: bool = self.elReyEstaEnJaque(color)!=None
        self.moverPieza(posFinal, posInicial,"")

        self[posFinal] = respaldo
        return estadoDeJaque