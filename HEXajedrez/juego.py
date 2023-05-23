import pygame
from typing import Optional
from tablero import Tablero
from hexCoord import HexCoord
from hexCelda import HexCelda
from pixel import PixelCoord
from hexPixelAdaptador import HexPixelAdaptador
from piezas import Piezas
from boton import Boton
from imagen import Imagen


class Juego:

    def __init__(self, x, colores: str):
        """Constructor de clase Juego."""
        # Dimension del juego.
        self.AREA_JUEGO: PixelCoord = PixelCoord(x*0.63, x*0.63)
        # Dimension adicional necesaria para la GUI.
        self.AREA_ESTADO: PixelCoord = PixelCoord(x*0.36, 0)
        self.piezas = Piezas(colores)

    def iniciar(self):
        """Iniciar el juego."""
        pygame.init()
        # Dimension del juego.
        AREA_JUEGO = self.AREA_JUEGO
        # Dimension adicional necesaria para la GUI.
        AREA_ESTADO = self.AREA_ESTADO
        # Fuente de AREA_ESTADO
        FUENTE = pygame.font.Font("fnt/8-Bit.TTF", 10)
        # Ancho y alto del juego.
        ANCHO_JUEGO, ALTO_JUEGO = AREA_JUEGO
        ANCHO_ESTADO = AREA_ESTADO[0]
        # Origen central del juego.
        ORIGEN_JUEGO: PixelCoord = AREA_JUEGO/2
        # Pantalla del juego.
        PANTALLA = pygame.display.set_mode(
            (ANCHO_JUEGO+ANCHO_ESTADO, ALTO_JUEGO))
        # Tablero de juego.
        HEX_TABLERO: Tablero = Tablero.generarMcCooey("bn")
        # El radio de un hexagono individual en pantalla, en pixeles.
        HEX_RADIO: float = 35.5
        # Lista de los colores de las celdas.
        HEX_COLORES: list[tuple] = [
            (60, 120, 60), (40, 40, 200), (184, 40, 50)]

        # Adapta los hexagonos a pixeles.
        ADAPTADOR: HexPixelAdaptador = HexPixelAdaptador(
            AREA_JUEGO, ORIGEN_JUEGO, HEX_RADIO)
        AREA_PIEZA: PixelCoord = PixelCoord(60, 60) / 2

        piezas = self.piezas
        imagenesDePiezas = piezas.piezasImagenes(piezas.colores)

        # El estado de la pieza seleccionada.
        piezaSeleccionada: Optional[HexCoord] = None
        # Cuando se elige una pieza guarda la coordena inicial de la pieza tomada.
        coordPiezaInicial: Optional[HexCoord] = None
        # Guarda los movimientos validos de la pieza tomada.
        movimientosValidos: Optional[list[HexCoord]] = None

        self.turnoJugador: int = 0  # Describe de quien es el turno (0: Blanco, 1: Negro, 2: Rojo).
        estadoRey: str = ""  # Un mensaje sobre el estado de cualquiera de los reyes..
        turnoTexto: str = ""  # Mensaje de qué lado es el turno.
        
        registroMovimientos = [] # Lista de movimientos realizados por todos los jugadores.
        desplazamientoRegistro = 0

        desplazamientoArribaImg = Imagen("img/boton_Arriba.png")
        desplazamientoAbajoImg = Imagen("img/boton_Abajo.png")

        botonDesplazamientoArriba = Boton(1060, 5, desplazamientoArribaImg.obtenerImagen(), .05)
        botonDesplazamientoAbajo = Boton(1060, 600, desplazamientoAbajoImg.obtenerImagen(), .05)

        @staticmethod
        def actualizarRegistro(movimiento, registro) -> bool:
            if movimiento != None:
                registro.append(movimiento)
            return len(registro) > 13

        def dibujaHex(coordenada: HexCoord, color: tuple, llenar=False):
            """Dibuja un hexagono en la pantalla."""
            pygame.draw.polygon(PANTALLA, color, ADAPTADOR.getVertices(
                coordenada), 0 if llenar else 3)

        def dibujarPiezas(celda: HexCelda):
            """Dibuja una pieza en pantalla segun la celd ingresada."""
            pixelCoords: PixelCoord = ADAPTADOR.hexAPixel(celda.coordenada)

            if celda.estado is not None:
                if celda.coordenada == coordPiezaInicial:
                    return
                PANTALLA.blit(
                    imagenesDePiezas[celda.estado], pixelCoords - AREA_PIEZA)
                
        def actualizaElTurno():
            """Comprueba las jugadas realizadas y así determina de qué lado es el turno."""

            self.turnoJugador = HEX_TABLERO.turno % len(self.piezas.colores)
            if self.turnoJugador < 1:
                self.turnoTexto = "Blanco"
            elif self.turnoJugador == 1:
                self.turnoTexto = "Negro" 
            else:
                self.turnoTexto ="Rojo" 
                
            if HEX_TABLERO.elReyEstaEnJaque('b'):
                if HEX_TABLERO.elReyEstaEnJaqueMate('b'):
                    self.estadoRey = "Jaque Mate al Rey Blanco"
                else:
                    self.estadoRey = "Jaque al Rey Blanco"
            elif HEX_TABLERO.elReyEstaEnJaque('n'):
                if HEX_TABLERO.elReyEstaEnJaqueMate('n'):
                    self.estadoRey = "Jaque Mate al Rey Negro"
                else:
                    self.estadoRey = "Jaque al Rey Negro"
            elif HEX_TABLERO.elReyEstaEnJaque('r'):
                if HEX_TABLERO.elReyEstaEnJaqueMate('r'):
                    self.estadoRey = "Jaque Mate al Rey Rojo"
                else:
                    self.estadoRey = "Jaque al Rey Rojo"
            else:
                self.estadoRey = ""
                
        def escribeTexto(texto: str,tamanio: int, x: any, y: any, colorTexto):
            """ Genenera un texto en pantalla con la FUENTE y color de texto elegidos en la 
            posicion "x" e "y" de la pantalla con el texto elegido. """
            img = pygame.font.Font("fnt/8-Bit.TTF", tamanio).render(texto, True, colorTexto)
            PANTALLA.blit(img, (x, y) )  

        juegoEjecutandose = True
        actualizaElTurno()
        # Bucle del juego:
        while juegoEjecutandose:
            for evento in pygame.event.get():
                # Si se pulsa la cruz para salir, se cierra la ventana y el programa.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if evento.type == pygame.MOUSEBUTTONUP:

                    # Traduce las coordenadas ingresadas a coordenadas axiales / hexagonales.
                    pixcelSeleccionado: PixelCoord = PixelCoord(
                        *pygame.mouse.get_pos())
                    coordSeleccion: HexCoord = round(
                        ADAPTADOR.pixelAHex(pixcelSeleccionado))

                    # Se verifica que el hexagono seleccionado no se encuentre fuera del tablero.
                    if coordSeleccion not in HEX_TABLERO:
                        continue

                    # Se obtiene el estado de seleccion del hexagono seleccionado.
                    piezaEnHexagono: Optional[str] = HEX_TABLERO[coordSeleccion]

                    # Si no hemos tomado una pieza:
                    if not piezaSeleccionada:
                        # Si no hay nada que tomar:
                        if piezaEnHexagono is None:
                            continue

                        # Obtener el color de la pieza seleccionada.
                        color: str = piezaEnHexagono[0]

                        # Verificar los turnos.
                        if not ((self.turnoJugador==0 and color == "b") or (self.turnoJugador==1 and color == "n") or (self.turnoJugador==2 and color == "r")):
                            continue

                        piezaSeleccionada = piezaEnHexagono
                        coordPiezaInicial = coordSeleccion
                        movimientosValidos = HEX_TABLERO.generarMovimientos(
                            coordPiezaInicial)

                    # De otro modo, se realizo clic con una pieza en mano.
                    else:
                        if coordSeleccion in movimientosValidos:
                            nuevoMov = HEX_TABLERO.moverPieza(
                                coordPiezaInicial, coordSeleccion, "jugador")
                            if actualizarRegistro(nuevoMov, registroMovimientos): desplazamientoRegistro = len(registroMovimientos) - 13
                            
                            piezaSeleccionada = coordPiezaInicial = None
                            actualizaElTurno()
            # se pone la pantalla de color blanco
            PANTALLA.fill((255, 255, 255))

            # se muestra la pantalla del juego con la imagen "Fondo_Juego.jpg"
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(
                f"img/Fondo_Estado.png").convert_alpha(), (410, 710)), (690, -5))
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(
                f"img/Fondo_Juego.png").convert_alpha(), (700, 700)), (-5, -2))

            # Dibuja los hexagonos de color.
            for celda in HEX_TABLERO:
                color: tuple[int, int, int] = HEX_COLORES[(
                    celda.coordenada.q - celda.coordenada.r) % 3]
                dibujaHex(celda.coordenada, color, llenar=True)

            # Dibuja los colores segun el estado del movimiento. Verde: movimientos posibles, Rojo: capturar piezas, Azul: celda actual.
            if coordPiezaInicial is not None:
                for coord in movimientosValidos:
                    color: tuple[int, int, int] = (
                        255, 50, 50) if HEX_TABLERO[coord] else (50, 255, 50)
                    dibujaHex(coord, color, llenar=True)

                dibujaHex(coordPiezaInicial, (50, 50, 255), llenar=True)

            # Dibuja el borde negro de los hexagonos y dibuja las piezas.
            for celda in HEX_TABLERO:
                dibujaHex(celda.coordenada, (20, 20, 20))
                dibujarPiezas(celda)

            # Si estamos sosteniendo una pieza se dibuja en la posicion del mouse.
            if piezaSeleccionada:
                PANTALLA.blit(
                    imagenesDePiezas[piezaSeleccionada], pygame.mouse.get_pos())

            # Se dibuja la linea que va a separar el tablero con la interfaz de turnos.
            pygame.draw.line(PANTALLA, (62, 48, 92),
                             (ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_JUEGO), 13)

            # Dibuja los movimientos guardados en el registro
            for i in range(13):
                if 0 <= (i + desplazamientoRegistro) < len(registroMovimientos):
                    escribeTexto(registroMovimientos[i + desplazamientoRegistro], 15 , (ANCHO_JUEGO + 30) , (145 + i * 35), (255,255,255))

            if botonDesplazamientoArriba.dibujar(""):
                if desplazamientoRegistro > 0: 
                            desplazamientoRegistro -= 1
            elif botonDesplazamientoAbajo.dibujar(""):
                desplazamientoRegistro += 1

            # Describe de quien es el turno:
            escribeTexto("Turno del jugador", 20, (ANCHO_JUEGO+30), 38,(255,255,255))
            escribeTexto(self.turnoTexto, 20, (ANCHO_JUEGO+140), 64,(255,255,255))
            # Describe el estado de Jaque:
            escribeTexto(self.estadoRey, 15, (ANCHO_JUEGO+45+len(self.estadoRey)), 95,(255,255,255))
            
            # Actualiza la pantalla.
            pygame.display.flip()

    print("juego iniciado")
