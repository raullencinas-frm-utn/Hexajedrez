import pygame
from typing import Optional
from tablero import Tablero
from hexCoord import HexCoord
from hexCasilla import HexCasilla
from pixel import PixelCoord
from hexPixelAdaptador import HexPixelAdaptador
from piezas import Piezas

class Juego:
    
    def __init__(self,x,colores: str):
        """Constructor de clase Juego."""
        # Dimension del juego.
        self.AREA_JUEGO:PixelCoord = PixelCoord(x*0.63, x*0.63)  
        # Dimension adicional necesaria para la GUI.
        self.AREA_ESTADO:PixelCoord = PixelCoord(x*0.36, 0)
        self.piezas = Piezas(colores) 
        

    def iniciar(self):
        """Iniciar el juego."""
        pygame.init()
        # Dimension del juego.
        AREA_JUEGO= self.AREA_JUEGO 
        # Dimension adicional necesaria para la GUI.
        AREA_ESTADO= self.AREA_ESTADO  
        # Ancho y alto del juego.
        ANCHO_JUEGO, ALTO_JUEGO = AREA_JUEGO
        ANCHO_ESTADO = AREA_ESTADO[0]
        # Origen central del juego.
        ORIGEN_JUEGO:PixelCoord = AREA_JUEGO/2
        # Pantalla del juego. 
        PANTALLA = pygame.display.set_mode((ANCHO_JUEGO+ANCHO_ESTADO,ALTO_JUEGO))
        HEX_TABLERO: Tablero = Tablero.generarMcCooey("wb")  # Tablero de juego.
        HEX_RADIO: float = 35.5  # El radio de un hexagono individual en pantalla, en pixeles.
        HEX_COLORES: list[tuple] = [(60, 120, 60),(40, 40, 200),(184, 40, 50)]  # Lista de los colores de las casillas.

        ADAPTADOR: HexPixelAdaptador = HexPixelAdaptador(AREA_JUEGO, ORIGEN_JUEGO, HEX_RADIO)  # Adapta los hexagonos a pixeles.
        AREA_PIEZA: PixelCoord = PixelCoord(60, 60) / 2 
        
        piezas = self.piezas
        imagenesDePiezas = piezas.piezasImagenes(piezas.colores)

        piezaSeleccionada: Optional[HexCoord] = None   # El estado de la pieza seleccionada.
        coordPiezaInicial: Optional[HexCoord] = None   # Cuando se elige una pieza guarda la coordena inicial de la pieza tomada       piezaSeleccionada: Optional[HexCoord] = None  # Guarda el estado(nombre) de la pieza tomada
        movimientosValidos: Optional[list[HexCoord]] = None   # Guarda los movimientos validos de la pieza tomada
        
        
        def dibujaHex(coordenada: HexCoord, color: tuple, llenar=False):
            """Dibuja un hexagono en la pantalla."""
            pygame.draw.polygon(PANTALLA, color , ADAPTADOR.getVertices(coordenada), 0 if llenar else 3)
            
        def dibujarPiezas(casilla: HexCasilla):
            """Dibuja una pieza en pantalla segun la casilla ingresada."""
            pixelCoords: PixelCoord = ADAPTADOR.hexAPixel(casilla.coordenada)
            
            if casilla.estado is not None:
                if casilla.coordenada == coordPiezaInicial: return
                PANTALLA.blit(imagenesDePiezas[casilla.estado], pixelCoords - AREA_PIEZA)

        juegoEjecutandose = True
        
        # Bucle del juego:
        while juegoEjecutandose:
            for evento in pygame.event.get():
                # Si se pulsa la cruz para salir, se cierra la ventana y el programa.
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if evento.type == pygame.MOUSEBUTTONUP:

                    # Traduce las coordenadas ingresadas a coordenadas axiales / hexagonales.
                    pixcelSeleccionado: PixelCoord = PixelCoord(*pygame.mouse.get_pos())
                    coordSeleccion: HexCoord = round(ADAPTADOR.pixelAHex(pixcelSeleccionado))

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
                        
                        piezaSeleccionada = piezaEnHexagono
                        coordPiezaInicial = coordSeleccion
                        movimientosValidos = HEX_TABLERO.generarMovimientos(coordPiezaInicial)

                    # De otro modo, se realizo clic con una pieza en mano.
                    else:
                        if coordSeleccion in movimientosValidos:
                            HEX_TABLERO.moverPieza(coordPiezaInicial, coordSeleccion, "jugador")
                            piezaSeleccionada = coordPiezaInicial = None
            
            # se pone la pantalla de color blanco
            PANTALLA.fill((255,255,255))
            
            # se muestra la pantalla del juego con la imagen "Fondo_Juego.jpg"
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Estado.png").convert_alpha(),(410, 710)),(690,0))
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Juego.png").convert_alpha(),(700, 700)),(-5,-2))
            
            # Dibuja los hexagonos de color.
            for casilla in HEX_TABLERO:
                color: tuple[int, int, int] = HEX_COLORES[(casilla.coordenada.q - casilla.coordenada.r) % 3]
                dibujaHex(casilla.coordenada, color, llenar=True)

            # Draw the valid moves for the current piece. Green = move, red = capture, blue = starting hex.
            if coordPiezaInicial is not None:
                for coord in movimientosValidos:
                    color: tuple[int, int, int] = (255, 50, 50) if HEX_TABLERO[coord] else (50, 255, 50)
                    dibujaHex(coord, color, llenar=True)

                dibujaHex(coordPiezaInicial, (50, 50, 255), llenar=True)
                
            # Dibuja el borde negro de los hexagonos y dibuja las piezas.
            for casilla in HEX_TABLERO:
                dibujaHex(casilla.coordenada, (20, 20, 20))
                dibujarPiezas(casilla)
            
            # Si estamos sosteniendo una pieza se dibuja en la posicion del mouse.
            if piezaSeleccionada:
                PANTALLA.blit(imagenesDePiezas[piezaSeleccionada], pygame.mouse.get_pos())
            
            # Se dibuja la linea que va a separar el tablero con la interfaz de turnos.
            pygame.draw.line(PANTALLA,(62,48,92),(ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_JUEGO),13)


            # Actualiza la pantalla.
            pygame.display.flip()


    print("juego iniciado")