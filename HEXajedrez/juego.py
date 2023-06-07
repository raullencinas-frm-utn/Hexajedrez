import pygame
import random
from typing import Optional
from tablero import Tablero
from hexCoord import HexCoord
from hexCelda import HexCelda
from pixel import PixelCoord
from hexPixelAdaptador import HexPixelAdaptador
from piezas import Piezas
from boton import Boton
from imagen import Imagen
from sonido import Sonidos
from musica import Musica

class Juego:

    def __init__(self, x, colores: str, ia: bool, continuar: bool, sonidoActivado: bool, musicaActivado: bool):

        """Constructor de clase Juego."""
    
        if continuar:
            linea:str = open("../Registro de jugadas.txt","r").readline().split(" ")
            colores = linea[0]
            ia = linea[1]=="True"
        # Dimension del juego.
        self.AREA_JUEGO: PixelCoord = PixelCoord(x*0.63, x*0.63)
        # Dimension adicional necesaria para la GUI.
        self.AREA_ESTADO: PixelCoord = PixelCoord(x*0.36, 0)
        self.ORIGEN_JUEGO: PixelCoord = self.AREA_JUEGO/2
        self.hex_radio: float = 35.5
        self.piezas = Piezas(colores)
        self.ia = ia


        self.continuar = continuar
        self.adaptador: HexPixelAdaptador = HexPixelAdaptador(self.AREA_JUEGO, self.ORIGEN_JUEGO, self.hex_radio)
        self.Musica = Musica("sonido/musica/")
        self.reproducir_sonidos = sonidoActivado
        self.reproducir_musica = musicaActivado
        self.Musica.iniciar(self.reproducir_musica)

    def iniciar(self, dificultad: str, pausa, juegoEjecutandose):
        Sonidos().sonidoIniciarJuego(self.reproducir_sonidos)
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
        ORIGEN_JUEGO: self.ORIGEN_JUEGO
        # Pantalla del juego.
        PANTALLA = pygame.display.get_surface()
        # Tablero de juego.
        HEX_TABLERO: Tablero = Tablero.generarMcCooey(self.piezas.colores)
        # El radio de un hexagono individual en pantalla, en pixeles.
        HEX_RADIO: self.hex_radio
        # Lista de los colores de las celdas.

        HEX_COLORES: list[tuple] = [
            (60, 120, 60), (40, 40, 200), (184, 40, 50)]

        # Adapta los hexagonos a pixeles.
        ADAPTADOR: HexPixelAdaptador = self.adaptador
        AREA_PIEZA: PixelCoord = PixelCoord(60, 60) / 2

        piezas = self.piezas
        imagenesDePiezas = piezas.piezasImagenes(piezas.colores)

        # El estado de la pieza seleccionada.

        piezaSeleccionada: Optional[HexCoord] = None

        # Cuando se elige una pieza guarda la coordena inicial de la pieza tomada.

        coordPiezaInicial: Optional[HexCoord] = None

        # Guarda los movimientos validos de la pieza tomada.

        movimientosValidos: Optional[list[HexCoord]] = None
        self.juegoEjecutandose = juegoEjecutandose
        self.turnoJugador: int = 0
        
        # Describe de quien es el turno (0: Blanco, 1: Negro, 2: Rojo).
        
        estadoRey: str = ""
        
        # Un mensaje sobre el estado de cualquiera de los reyes..
        
        turnoTexto: str = "" 
        
        # Mensaje de qué lado es el turno.
        
        registroMovimientos = [] 
        
        # Lista de movimientos realizados por todos los jugadores.
        
        desplazamientoRegistro = 0

        desplazamientoArribaImg = Imagen("img/boton_Arriba.png")
        desplazamientoAbajoImg = Imagen("img/boton_Abajo.png")

        botonDesplazamientoArriba = Boton(1030, 125, desplazamientoArribaImg.obtenerImagen(), .75)
        botonDesplazamientoAbajo = Boton(1030, 650, desplazamientoAbajoImg.obtenerImagen(), .75)

        @staticmethod
        def actualizarRegistro(movimiento, registro) -> bool:

            """Se actualiza el historial de movimientos con el movimiento que se pasa como parametro."""

            if movimiento != None:
                registro.append(movimiento)
            return len(registro) > 15

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

        juegoEjecutandose [0] = True
        actualizaElTurno()

        # Bucle del juego:

        while self.juegoEjecutandose[0]:
            if self.reproducir_musica:
                if not pygame.mixer.music.get_busy():
                    siguiente_cancion = random.choice(self.lista_canciones)
                    pygame.mixer.music.load(siguiente_cancion)
                    pygame.mixer.music.play(-1)
            for evento in pygame.event.get():

                # Si se pulsa la cruz para salir, se cierra la ventana y el programa.

                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pausa[0] = not pausa[0]
                        juegoEjecutandose[0] = False
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
                        Sonidos().sonidoTomarPieza(self.reproducir_sonidos)
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
                            Sonidos().sonidoSoltarPieza(self.reproducir_sonidos)
                            nuevoMov = HEX_TABLERO.moverPieza(
                                coordPiezaInicial, coordSeleccion, "jugador")
                            if actualizarRegistro(nuevoMov, registroMovimientos): desplazamientoRegistro = len(registroMovimientos) - 15
                            
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
                             (ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_JUEGO), 15)

            # Dibuja los movimientos guardados en el registro

            for i in range(15):
                if 0 <= (i + desplazamientoRegistro) < len(registroMovimientos):
                    escribeTexto(registroMovimientos[i + desplazamientoRegistro], 15 , (ANCHO_JUEGO + 30) , (145 + i * 35), (255,255,255))

            if botonDesplazamientoArriba.dibujar("", self.reproducir_sonidos):
                if desplazamientoRegistro > 0: 
                            desplazamientoRegistro -= 1
            
            if botonDesplazamientoAbajo.dibujar("", self.reproducir_sonidos):
                desplazamientoRegistro += 1

            # Describe de quien es el turno:

            escribeTexto("Turno del jugador", 20, (ANCHO_JUEGO+30), 38,(255,255,255))
            escribeTexto(self.turnoTexto, 20, (ANCHO_JUEGO+140), 64,(255,255,255))

            # Describe el estado de Jaque:

            escribeTexto(self.estadoRey, 15, (ANCHO_JUEGO+45+len(self.estadoRey)), 95,(255,255,255))
            
            # Actualiza la pantalla.

            pygame.display.flip()

