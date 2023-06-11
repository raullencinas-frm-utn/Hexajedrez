import math
import random
import pygame
from typing import Optional
from hexCelda import HexCelda
from hexCoord import HexCoord
from tablero import Tablero
from imagen import Imagen
from hexPixelAdaptador import HexPixelAdaptador



class Bot:
    """Clase que realiza los movimientos de la CPU."""
    cacheMinimax = dict()
    cacheValorPorPosicion = dict()

    def __init__(self, color :str, dificultad :str, adaptador :HexPixelAdaptador, unSoloBot :bool) -> None:
        self.color = color
        self.enemigo = "n" if color=="r" else "r"
        self.unSoloBot = unSoloBot
        self.profundidad = 2 if dificultad=="Facil" else 4 if dificultad=="Medio" else 8
        self.adaptador = adaptador

    def mover(self, tablero: Tablero) -> tuple[HexCoord, HexCoord]:
        """Hace un movimiento en el tablero tras realizar una búsqueda minimax."""
        mayorPuntuacion: float = -math.inf
        mejorMovimiento: Optional[tuple] = None
        
        for (posInicial, posFinal) in tablero.movimientosPorColor(self.color):
            
            tableroRespaldo = tablero[posFinal]
            tablero.moverPieza(posInicial, posFinal, "")
            resultado: float = self.minimax(tablero, self.profundidad, -math.inf, math.inf, 1)
            
            tablero.moverPieza(posFinal, posInicial, "")
            tablero[posFinal] = tableroRespaldo

            if resultado > mayorPuntuacion:
                mayorPuntuacion = resultado
                mejorMovimiento = (posInicial, posFinal)

            elif resultado == mayorPuntuacion:
                if random.choice((False,True)):
                    mayorPuntuacion = resultado
                    mejorMovimiento = (posInicial, posFinal)

        
        if mejorMovimiento==None:
            return

        registro=tablero.moverPieza(*mejorMovimiento, "Bot")

        # Se guardan los valores para dibujar la pieza.
        reloj = pygame.time.Clock()
        piezaAMover = tablero[mejorMovimiento.__getitem__(1)]
        imagenBot = Imagen(f"img/{piezaAMover}.png").obtenerImagen()
        coordenadas_iniciales = self.adaptador.hexAPixel(mejorMovimiento.__getitem__(0))
        coordenadas_finales = self.adaptador.hexAPixel(mejorMovimiento.__getitem__(1))
        dx = coordenadas_finales[0] - coordenadas_iniciales[0]
        dy = coordenadas_finales[1] - coordenadas_iniciales[1]
        distancia = math.sqrt(dx**2 + dy**2)

        fotogramas_totales = int(distancia / 5)  # Ajusta el valor 5 para cambiar la velocidad
        desplazamiento_x = dx / fotogramas_totales
        desplazamiento_y = dy / fotogramas_totales

        x, y = coordenadas_iniciales
        copia_superficie = pygame.display.get_surface().copy()
        capa = pygame.Surface((self.adaptador.dimensiones), pygame.SRCALPHA)
        

        # Dibujar la copia en la ventana
   
        for _ in range(fotogramas_totales):
            x += desplazamiento_x
            y += desplazamiento_y

            # Realizar cualquier otra lógica de juego aquí

            # Dibujar la imagen en la pantalla
            imagenBot.set_alpha(200)  # Ajusta el valor de 0 a 255 para cambiar la transparencia
            
            capa.blit(copia_superficie,(0,0))
            capa.blit(imagenBot,((x-30), (y-30)))
            pygame.display.get_surface().blit(capa, (0, 0))
            pygame.display.flip()
            reloj.tick(90)
        
        return (mejorMovimiento, registro)
    
    def valorPorPosicion(self, celda: HexCelda) -> int:
        """Se devuelve el valor de la posición."""
        hashEstado = hash(celda.__str__())
        if hashEstado in self.cacheValorPorPosicion:
            return self.cacheValorPorPosicion[hashEstado]

        """Evalúa la puntuacion de las pieza segun su posicionamiento en el tablero."""
        # Se crean diccionarios con puntos para cada posición del tablero de cada pieza.
        if celda.estado[2:]=="peon":
            valores: dict[int, list[tuple]] = {
                0: [(-3, -2, 5),(-2, -3, 5),(-1, -4, 5),(0, -5, 5),(1, -5, 4),(2, -5, 3),(3, -5, 2)],
                10: [(-5, 0, 5),(-5, 1, 4),(-4, -1, 5),(-4, 0, 4),(-4, 1, 3),(-3, -1, 4),(-3, 0, 3),(-3, 1, 2),(-2, -2, 4),(-2, -1, 3),(-2, 0, 2),(-2, 1, 1),(-1, -4, 5),(-1, -3, 4),(-1, -2, 3),(-1, -1, 2),(-1, 0, 1),(0, -5, 5),(0, -5, 5),(0, -4, 4),(0, -3, 3),(0, -2, 2),(0, -1, 1),(1, -5, 4),(1, -4, 3),(1, -3, 2),(1, -2, 1),(1, -1, 0),(2, -4, 2),(2, -3, 1),(2, -2, 0),(2, -1, -1),(3, -4, 1),(3, -3, 0),(3, -2, -1),(4, -5, 1),(4, -4, 0),(4, -3, -1),(5, -5, 0),(5, -4, -1)],
                15: [(-5, 2, 3),(-4, 2, 2),(-3, 2, 1),(-2, 2, 0),(-1, 1, 0),(0, 0, 0),(1, 0, -1),(2, 0, -2),(3, -1, -2),(4, -2, -2),(-5, 3, 2),(-4, 3, 1),(-3, 3, 0),(-2, 3, -1),(-1, 2, -1),(0, 1, -1),(1, 1, -2),(2, 1, -3),(3, 0, -3),(4, -1, -3),(5, -2, -3),(5, -3, -2)],     
                30: [(-5, 4, 1),(-4, 4, 0),(-3, 4, -1),(-2, 4, -2),(-1, 3, -2),(0, 2, -2),(1, 2, -3),(2, 2, -4),(3, 1, -4),(4, 0, -4),(5, -1, -4)],
                500: [(-5, 5, 0),(-4, 5, -1),(-3, 5, -2),(-2, 5, -3),(-1, 4, -3),(0, 3, -3),(1, 3, -4),(2, 3, -5),(3, 2, -5),(4, 1, -5),(5, 0, -5)]
        }
        
        elif celda.estado[2:]=="caballo":
            valores: dict[int, list[tuple]] = {
                2: [(-5, 0, 5),(5, -5, 0)],
                4: [(-5, 1, 4),(-5, 5, 0),(-4, -1, 5),(4, -5, 1),(5, -4, -1),(5, 0, -5)],
                6: [(-5, 2, 3),(-5, 4, 1),(-4, 0, 4),(-4, 5, -1),(-3, -2, 5),(3, -5, 2),(4, -4, 0),(4, 1, -5),(5, -3, -2),(5, -1, -4)],
                7: [(-5, 3, 2),(-4, 1, 3),(-4, 4, 0),(-3, -1, 4),(-3, 5, -2),(-2, -3, 5),(2, -5, 3),(3, -4, 1),(3, 2, -5),(4, -3, -1),(4, 0, -4),(5, -2, -3)],
                8: [(-4, 2, 2),(-4, 3, 1),(-3, 0, 3),(-3, 4, -1),(-2, -2, 4),(-2, 5, -3),(-1, -4, 5),(1, -5, 4),(2, -4, 2),(2, 3, -5),(3, -3, 0),(3, 1, -4),(4, -2, -2),(4, -1, -3)],
                9: [(-3, 1, 2),(-3, 3, 0),(-1, -3, 4),(-1, -4, 5),(0, -5, 5),(1, -4, 3),(1, -5, 4),(3, -2, -1),(3, 0, -3)],
                10: [(-3, 2, 1),(0, -4, 4),(0, -5, 5),(3, -1, -2)],
                15: [(-2, -1, 3),(-2, 4, -2),(-1, -2, 3),(-1, 4, -3),(1, -3, 2),(1, 3, -4),(2, -3, 1),(2, 2, -4)],
                30: [(-2, 0, 2),(-2, 3, -1),(-1, -1, 2),(-1, 3, -2),(1, -2, 1),(1, 2, -3),(2, -2, 0),(2, 1, -3)],
                50: [(-1, 1, 0),(0, -1, 1),(0, 0, 0),(0, 1, -1),(0, 2, -2),(1, 0, -1)],
                40: [(-2, 1, 1),(-2, 2, 0),(-1, 0, 1),(-1, 2, -1),(0, -2, 2),(0, 3, -3),(1, -1, 0),(1, 1, -2),(2, -1, -1),(2, 0, -2)],
                20: [(0, -3, 3),(0, -5, 5)]
            }
        
        elif celda.estado[2:]=="alfil":
            valores: dict[int, list[tuple]] = {
                5: [(-4, -1, 5),(4, -5, 1)],
                10: [(-5, 0, 5),(-4, 0, 4),(-4, 5, -1),(-3, -2, 5),(-1, -4, 5),(1, -5, 4),(3, -5, 2),(4, -4, 0),(4, 1, -5),(5, -5, 0)],
                15: [(-5, 1, 4),(-4, 1, 3),(-4, 4, 0),(-3, -1, 4),(-3, 5, -2),(-2, -3, 5),(-1, -3, 4),(-1, -4, 5),(1, -4, 3),(1, -5, 4),(2, -5, 3),(3, -4, 1),(3, 2, -5),(4, -3, -1),(4, 0, -4),(5, -4, -1)],
                40: [(-5, 4, 1),(-3, 2, 1),(-2, -1, 3),(-2, 1, 1),(-2, 4, -2),(0, -5, 5),(0, -4, 4),(0, -3, 3),(0, -2, 2),(0, -1, 1),(0, 0, 0),(0, 1, -1),(0, 2, -2),(0, 3, -3),(0, -5, 5),(0, -5, 5),(2, -3, 1),(2, -1, -1),(2, 2, -4),(3, -1, -2),(5, -1, -4)],
                60: [(-5, 3, 2),(-5, 5, 0),(-3, 1, 2),(-3, 3, 0),(-2, 0, 2),(-2, 3, -1),(-1, -1, 2),(-1, 3, -2),(1, -2, 1),(1, 2, -3),(2, -2, 0),(2, 1, -3),(3, -2, -1),(3, 0, -3),(5, -2, -3),(5, 0, -5)],
                70: [(-2, 2, 0),(-1, 0, 1),(-1, 1, 0),(-1, 2, -1),(1, -1, 0),(1, 0, -1),(1, 1, -2),(2, 0, -2)],
                20: [(-4, 2, 2),(-4, 3, 1),(-2, -2, 4),(-2, 5, -3),(-1, -2, 3),(-1, 4, -3),(1, -3, 2),(1, 3, -4),(2, -4, 2),(2, 3, -5),(4, -2, -2),(4, -1, -3)],
                30: [(-5, 2, 3),(-3, 0, 3)]
            }
        
        elif celda.estado[2:]=="torre":
            valores: dict[int, list[tuple]] = {
                10: [(-5, 0, 5),(-5, 5, 0),(0, -5, 5),(0, 3, -3),(5, -5, 0),(5, 0, -5)],
                100: [(-5, 1, 4),(-5, 2, 3),(-5, 3, 2),(-5, 4, 1),(-4, 0, 4),(-4, 1, 3),(-4, 2, 2),(-4, 3, 1),(-4, 4, 0),(-3, -1, 4),(-3, 4, -1),(-2, -2, 4),(-2, 4, -2),(-1, -4, 5),(-1, 3, -2),(1, -5, 4),(1, 2, -3),(2, -4, 2),(2, 2, -4),(3, -4, 1),(3, 1, -4),(4, -4, 0),(4, -3, -1),(4, -2, -2),(4, -1, -3),(4, 0, -4),(5, -4, -1),(5, -3, -2),(5, -2, -3),(5, -1, -4)],
                120: [(-2, 0, 2),(-2, 1, 1),(-2, 2, 0),(-1, -2, 3),(-1, -1, 2),(-1, 0, 1),(-1, 1, 0),(0, -5, 5),(0, -4, 4),(0, -3, 3),(0, -2, 2),(0, -1, 1),(0, 0, 0),(0, 1, -1),(1, -3, 2),(1, -2, 1),(1, -1, 0),(1, 0, -1),(2, -2, 0),(2, -1, -1),(2, 0, -2)],
                110: [(-3, 0, 3),(-3, 1, 2),(-3, 2, 1),(-3, 3, 0),(-2, -1, 3),(-2, 3, -1),(-1, -3, 4),(-1, 2, -1),(0, -5, 5),(0, 2, -2),(1, -4, 3),(1, 1, -2),(2, -3, 1),(2, 1, -3),(3, -3, 0),(3, -2, -1),(3, -1, -2),(3, 0, -3)],
                80: [(-4, -1, 5),(-4, 5, -1),(-3, -2, 5),(-3, 5, -2),(-2, -3, 5),(-2, 5, -3),(-1, -4, 5),(-1, 4, -3),(1, -5, 4),(1, 3, -4),(2, -5, 3),(2, 3, -5),(3, -5, 2),(3, 2, -5),(4, -5, 1),(4, 1, -5)]
            }
            
        elif celda.estado[2:]=="dama":
            valores: dict[int, list[tuple]] = {
                150: [(-5, 0, 5),(-5, 5, 0),(5, -5, 0),(5, 0, -5)],
                170: [(-4, -1, 5),(-4, 5, -1),(0, -5, 5),(0, 3, -3),(4, -5, 1),(4, 1, -5)],
                190: [(-4, 0, 4),(-4, 4, 0),(-3, -2, 5),(-3, 5, -2),(-1, -4, 5),(-1, 4, -3),(0, -5, 5),(0, 2, -2),(1, -5, 4),(1, 3, -4),(3, -5, 2),(3, 2, -5),(4, -4, 0),(4, 0, -4)],
                220: [(-5, 1, 4),(-5, 4, 1),(-3, -1, 4),(-3, 0, 3),(-3, 3, 0),(-3, 4, -1),(-1, -4, 5),(-1, 3, -2),(1, -5, 4),(1, 2, -3),(3, -4, 1),(3, -3, 0),(3, 0, -3),(3, 1, -4),(5, -4, -1),(5, -1, -4)],
                250: [(-4, 1, 3),(-4, 2, 2),(-4, 3, 1),(-2, -2, 4),(-2, 4, -2),(0, -4, 4),(0, -3, 3),(0, -2, 2),(0, -1, 1),(0, 0, 0),(2, -4, 2),(2, 2, -4),(4, -3, -1),(4, -2, -2),(4, -1, -3)],
                260: [(-2, -1, 3),(-2, 0, 2),(-2, 1, 1),(-2, 2, 0),(-2, 3, -1),(2, -3, 1),(2, -2, 0),(2, -1, -1),(2, 0, -2),(2, 1, -3)],
                210: [(-2, -3, 5),(2, -5, 3)],
                230: [(-5, 2, 3),(-5, 3, 2),(-3, 1, 2),(-3, 2, 1),(-2, 5, -3),(-1, -3, 4),(-1, -2, 3),(-1, -1, 2),(-1, 0, 1),(-1, 1, 0),(-1, 2, -1),(0, -5, 5),(0, 1, -1),(1, -4, 3),(1, -3, 2),(1, -2, 1),(1, -1, 0),(1, 0, -1),(1, 1, -2),(2, 3, -5),(3, -2, -1),(3, -1, -2),(5, -3, -2),(5, -2, -3)]
            }
        
        else:
            valores: dict[int, list[tuple]] = {
                1870: [(-5, 0, 5),(-5, 5, 0),(0, -5, 5),(0, 3, -3),(5, -5, 0),(5, 0, -5)],
                1880: [(-5, 1, 4),(-5, 4, 1),(-4, -1, 5),(-4, 5, -1),(-2, -3, 5),(-2, 5, -3),(2, -5, 3),(2, 3, -5),(4, -5, 1),(4, 1, -5),(5, -4, -1),(5, -1, -4)],
                1900: [(-5, 2, 3),(-5, 3, 2),(-4, 1, 3),(-4, 2, 2),(-4, 3, 1),(-3, -1, 4),(-3, 0, 3),(-3, 1, 2),(-3, 2, 1),(-3, 3, 0),(-3, 4, -1),(-2, -2, 4),(-2, -1, 3),(-2, 3, -1),(-2, 4, -2),(-1, -4, 5),(-1, -3, 4),(-1, 2, -1),(-1, 3, -2),(0, -5, 5),(0, -5, 5),(0, 1, -1),(0, 2, -2),(1, -5, 4),(1, -4, 3),(1, 1, -2),(1, 2, -3),(2, -4, 2),(2, -3, 1),(2, 1, -3),(2, 2, -4),(3, -4, 1),(3, -3, 0),(3, -2, -1),(3, -1, -2),(3, 0, -3),(3, 1, -4),(4, -3, -1),(4, -2, -2),(4, -1, -3),(5, -3, -2),(5, -2, -3)],
                1920: [(-2, 0, 2),(-2, 1, 1),(-2, 2, 0),(-1, -2, 3),(-1, -1, 2),(-1, 0, 1),(-1, 1, 0),(0, -4, 4),(0, -3, 3),(0, -2, 2),(0, -1, 1),(0, 0, 0),(1, -3, 2),(1, -2, 1),(1, -1, 0),(1, 0, -1),(2, -2, 0),(2, -1, -1),(2, 0, -2)],
                1910: [(-1, -4, 5),(-1, 4, -3),(1, -5, 4),(1, 3, -4)],
                1890: [(-4, 0, 4),(-4, 4, 0),(-3, -2, 5),(-3, 5, -2),(3, -5, 2),(3, 2, -5),(4, -4, 0),(4, 0, -4)]
            }
        
        # Se gira el tablero dependiendo del punto de vista del color de la pieza elegida.
        for key in valores:
            if celda.estado[0]=="b":
                a,b,c = celda.coordenada.p, celda.coordenada.q, celda.coordenada.r
                
            elif celda.estado[0]=="n":
                if self.unSoloBot:
                    a,b,c = celda.coordenada.p, celda.coordenada.r, celda.coordenada.q
                else:
                    a,b,c = celda.coordenada.r, celda.coordenada.q, celda.coordenada.p
            
            else:
                a,b,c = celda.coordenada.r, celda.coordenada.p, celda.coordenada.q
                
            if (a,b,c) in valores[key]:
                self.cacheValorPorPosicion[hashEstado] = key
                return key

        return 1
    
    def minimax(self, HEX_TABLERO: Tablero, profundidad: int, alfa: float, beta: float, turno: int) -> float:
        pygame.event.pump()
        """Realiza una búsqueda minimax hasta una profundidad determinada."""
        hashEstado = hash(HEX_TABLERO.__str__())
        if hashEstado in self.cacheMinimax:
            return self.cacheMinimax[hashEstado]

        # Limite de la profundidad.
        if profundidad == 0:
            return self.evaluar(HEX_TABLERO)

        # Establece puntuación final como infinito negativo o infinito positivo según se trate de un movimiento propio del bot.
        puntuacionFinal: float = math.inf * (-1) ** (turno == 0)
        movimientos = ()

        if turno == 0:
            movimientos = HEX_TABLERO.movimientosPorColor(self.color)
        
        elif turno == 1:
            if HEX_TABLERO.elReyExiste("b"):
                # Prioriza ahogar / hacer Jaque Mate al rey blanco ante todo.
                if HEX_TABLERO.elReyEstaAhogado("b"):
                    return self.evaluar(HEX_TABLERO)
                movimientos = HEX_TABLERO.movimientosPorColor("b")
        
        else:
            if HEX_TABLERO.elReyExiste(self.enemigo):
                movimientos = HEX_TABLERO.movimientosPorColor(self.enemigo)

        contador = 0
        for (posInicial, posFinal) in movimientos:
            contador += 1
            tableroRespaldo = HEX_TABLERO[posFinal]
            HEX_TABLERO.moverPieza(posInicial, posFinal,"")
            resultado: float = self.minimax(HEX_TABLERO, ( profundidad - 1), alfa, beta, (turno+1)%len(HEX_TABLERO.piezas.colores))
            HEX_TABLERO.moverPieza(posFinal, posInicial,"")
            HEX_TABLERO[posFinal] = tableroRespaldo

            # Poda alfa-beta.
            if turno == 0:
                puntuacionFinal = max(resultado, puntuacionFinal)
                alfa = max(alfa, resultado)
            else:
                puntuacionFinal = min(resultado, puntuacionFinal)
                beta = min(beta, resultado)
            
            if alfa <= beta:
                break
        
        if contador == 0:
            resultado: float = self.minimax(HEX_TABLERO, ( profundidad - 1), alfa, beta, (turno+1)%len(HEX_TABLERO.piezas.colores))

            if turno == 0:
                puntuacionFinal = max(resultado, puntuacionFinal)
            else:
                puntuacionFinal = min(resultado, puntuacionFinal)

        self.cacheMinimax[hashEstado] = puntuacionFinal
        pygame.event.pump()
        return puntuacionFinal
    
    def evaluar(self, HEX_TABLERO: Tablero) -> float:
        """Evalua la puntuación del estado del tablero."""
        tableroAValores = lambda celda: self.valorPorPosicion(celda) * (1 if HEX_TABLERO.elReyExiste(celda.estado[0]) else 0)
        sumaValores = lambda col: sum(map(tableroAValores, HEX_TABLERO.celdasPiezasMismoColor(col)))
        modificador: int = 0
        
        if HEX_TABLERO.elReyEstaAhogado("b"):
            modificador = 2000
        elif HEX_TABLERO.elReyEstaEnJaque("b")!=None:
            modificador = 500
        elif HEX_TABLERO.elReyEstaAhogado(self.enemigo):
            modificador = 800
        elif HEX_TABLERO.elReyEstaEnJaque(self.enemigo)!=None:
            modificador = 500
        elif HEX_TABLERO.elReyEstaAhogado(self.color):
            modificador = -9999
        elif HEX_TABLERO.elReyEstaEnJaque(self.color)!=None:
            modificador = -500
        
        return +(sumaValores(self.color) - sumaValores("b") - sumaValores(self.enemigo)) + modificador
        