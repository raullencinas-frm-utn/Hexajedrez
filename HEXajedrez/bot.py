import math
import pygame
from typing import Optional
from hexCelda import HexCelda
from hexCoord import HexCoord
from tablero import Tablero
from imagen import Imagen
from hexPixelAdaptador import HexPixelAdaptador


class Bot:
    cont = 0
    cache = dict()
    
    def __init__(self, color :str, dificultad :str, adaptador :HexPixelAdaptador, unSoloBot :bool) -> None:
        self.color = color
        self.enemigo = "n" if color=="r" else "r"
        self.profundidad = 2 if dificultad=="Facil" else 4 if dificultad=="Medio" else 8
        esNegro = 1 if color=="n" else -1
        self.adaptador = adaptador
        self.unSoloBot = unSoloBot
    

        self.valoresDeCaptura = {
            None: 0,
            "b_peon": 10,
            "b_torre": 100,
            "b_rey": 900,
            "b_alfil": 60,
            "b_caballo": 30,
            "b_dama": 250,
            
            "r_peon": 10 * esNegro,
            "r_torre": 100 * esNegro,
            "r_rey": 900 * esNegro,
            "r_alfil": 60 * esNegro,
            "r_caballo": 30 * esNegro,
            "r_dama": 250 * esNegro,
            
            "n_peon": -10 * esNegro,
            "n_torre": -100 * esNegro,
            "n_rey": -900 * esNegro,
            "n_alfil": -60 * esNegro,
            "n_caballo": -30 * esNegro,
            "n_dama": -250 * esNegro,
        }
    
    def move(self, tablero: Tablero) -> tuple[HexCoord, HexCoord]:

        """Hace un movimiento en el tablero tras realizar una búsqueda minimax."""
        mayorPuntuacion: float = -math.inf
        mejorMovimiento: Optional[tuple] = None
        
        for (posInicial, posFinal) in tablero.movimientosPorColor(self.color):
            
            tableroRespaldo = tablero[posFinal]
            tablero.moverPieza(posInicial, posFinal, "")
            resultado: float = self.minimax(tablero, self.profundidad, -math.inf, math.inf, False)
            
            tablero.moverPieza(posFinal, posInicial, "")
            tablero[posFinal] = tableroRespaldo

            if resultado > mayorPuntuacion:
                mayorPuntuacion = resultado
                mejorMovimiento = (posInicial, posFinal)

        
        if mejorMovimiento==None:
            return

        registro=tablero.moverPieza(*mejorMovimiento, "Bot")
        reloj = pygame.time.Clock()
        piezaAMover = tablero[mejorMovimiento.__getitem__(1)]
        imagenBot = Imagen(f"img/{piezaAMover}.png").redimensionar(60, 60)
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
            reloj.tick(120)
        return (mejorMovimiento, registro)
    
    def minimax(self, HEX_TABLERO: Tablero, profundidad: int, alpha: float, beta: float, estaMaximizando: bool) -> float:
        """Realiza una búsqueda minimax hasta una profundidad determinada."""
        hashEstado = hash(HEX_TABLERO.__str__())
        if hashEstado in self.cache:
            return self.cache[hashEstado]

        # Limite de la profundidad.
        if profundidad == 0:
            return self.evaluar(HEX_TABLERO)

        # Establece puntuación final como infinito negativo o infinito positivo según esté maximizando o minimizando.
        puntuacionFinal: float = math.inf * (-1) ** estaMaximizando
        
        if estaMaximizando:
            movimientos = HEX_TABLERO.movimientosPorColor(self.color)
        else:
            movimientos = HEX_TABLERO.movimientosPorColor("b")
            if HEX_TABLERO.piezas.colores.endswith("r"):
                movimientos = tuple(movimientos)+tuple(HEX_TABLERO.movimientosPorColor(self.enemigo))
        
        for (posInicial, posFinal) in movimientos:
            self.cant = (self.cont+1)
            tableroRespaldo = HEX_TABLERO[posFinal]
            HEX_TABLERO.moverPieza(posInicial, posFinal,"")
            resultado: float = self.minimax(HEX_TABLERO, ( profundidad - 1), alpha, beta, not estaMaximizando)
            HEX_TABLERO.moverPieza(posFinal, posInicial,"")
            HEX_TABLERO[posFinal] = tableroRespaldo

            # Poda alfa-beta.
            if estaMaximizando:
                puntuacionFinal = max(resultado, puntuacionFinal)
                alpha = max(alpha, resultado)
            else:
                puntuacionFinal = min(resultado, puntuacionFinal)
                beta = min(beta, resultado)

            if alpha <= beta:
                break

        Bot.cache[hashEstado] = puntuacionFinal
        return puntuacionFinal

    def evaluar(self, HEX_TABLERO: Tablero) -> float:
        """Evalua la puntuación del estado del tablero."""
        tableroAValores = lambda celda: self.valoresDeCaptura[celda.estado] * (1 if HEX_TABLERO.elReyExiste(celda.estado[0]) else 0)
        sumaValores = lambda col: sum(map(tableroAValores, HEX_TABLERO.celdasPiezasMismoColor(col)))
        modificador: int = 0
        
        if HEX_TABLERO.elReyEstaEnJaque("b")!=None:
            if HEX_TABLERO.elReyEstaEnJaqueMate("b"):
                modificador = 800
            else:
                modificador = 500
        elif HEX_TABLERO.elReyEstaEnJaque(self.enemigo)!=None:
            if HEX_TABLERO.elReyEstaEnJaqueMate(self.enemigo):
                modificador = 800
            else:
                modificador = 500
        elif HEX_TABLERO.elReyEstaEnJaque(self.color)!=None:
            if HEX_TABLERO.elReyEstaEnJaqueMate(self.color):
                modificador = -9999
            else:
                modificador = -500
        elif HEX_TABLERO.elReyEstaAhogado("b") or HEX_TABLERO.elReyEstaAhogado(self.enemigo):
            modificador = 800
        
        return -(sumaValores(self.color) + sumaValores("b") +sumaValores(self.enemigo)) + modificador
        