import pygame
from tablero import Tablero
from hexCoord import HexCoord
from hexCasilla import HexCasilla
from pixel import PixelCoord
from hexPixelAdaptador import HexPixelAdaptador
class Juego:
    
    def __init__(self,x):
        # Dimensión del juego.
        self.AREA_JUEGO:PixelCoord = PixelCoord(x*0.63, x*0.63)  
        # Dimensión adicional necesaria para la GUI.
        self.AREA_ESTADO:PixelCoord = PixelCoord(x*0.36, 0) 
        

    def iniciar(self):
        pygame.init()
        # Dimensión del juego.
        AREA_JUEGO= self.AREA_JUEGO 
        # Dimensión adicional necesaria para la GUI.
        AREA_ESTADO= self.AREA_ESTADO  
        # Ancho y alto del juego.
        ANCHO_JUEGO, ALTO_JUEGO = AREA_JUEGO
        ANCHO_ESTADO, ALTO_ESTADO = AREA_ESTADO
        # Origen central del juego.
        ORIGEN_JUEGO:PixelCoord = AREA_JUEGO/2
        # Pantalla del juego. 
        PANTALLA = pygame.display.set_mode((ANCHO_JUEGO+ANCHO_ESTADO,ALTO_JUEGO))
        HEX_TABLERO: Tablero = Tablero.aPartirDeGlinski("wb")  # Tablero de juego.
        HEX_RADIO: float = 35.5  # El radio de un hexagono individual en pantalla, en pixeles.
        HEX_COLORES: list[tuple] = [(60, 120, 60),(40, 40, 200),(184, 40, 50)]  # Lista de los colores de las casillas.

        ADAPTADOR: HexPixelAdaptador = HexPixelAdaptador(AREA_JUEGO, ORIGEN_JUEGO, HEX_RADIO)  # Adapta los hexagonos a pixeles.
        

        def dibujaHex(coordenada: HexCoord, color: tuple, llenar=False):
            """Dibuja un hexagono en la pantalla."""
            pygame.draw.polygon(PANTALLA, color , ADAPTADOR.getVertices(coordenada), 0 if llenar else 3)

        juegoEjecutandose = True
        
        # Bucle del juego
        while juegoEjecutandose:
            for evento in pygame.event.get():
                #si se pulsa la cruz para salir, se cierra la ventana y el programa
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # se pone la pantalla de color blanco
            PANTALLA.fill((255,255,255))
            
            # se muestra la del juego con la imagen "Fondo_Juego.jpg"

            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Estado.png").convert_alpha(),(410, 710)),(690,0))
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Juego.png").convert_alpha(),(700, 700)),(-5,-2))
            
            # Dibuja los hexagonos de color.
            for casilla in HEX_TABLERO:
                color: tuple[int, int, int] = HEX_COLORES[(casilla.coordenada.q - casilla.coordenada.r) % 3]
                dibujaHex(casilla.coordenada, color, llenar=True)
            
            # Dibuja el borde negro.
            for casilla in HEX_TABLERO:
                dibujaHex(casilla.coordenada, (20, 20, 20))

            # se dibuja la linea que va a separar el tablero con la GUI de informacion
            pygame.draw.line(PANTALLA,(62,48,92),(ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_JUEGO),13)

            #actualiza la pantalla
            pygame.display.flip()


    print("juego iniciado")