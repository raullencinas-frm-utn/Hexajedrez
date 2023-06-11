import os
import pygame
import random

from typing import Optional
from bot import Bot
from tablero import Tablero
from hexCoord import HexCoord
from hexCelda import HexCelda
from pixel import PixelCoord
from hexPixelAdaptador import HexPixelAdaptador
from piezas import Piezas
from boton import Boton
from imagen import Imagen
from sonido import Sonido
from musica import Musica


class Juego:


    def __init__(self, x, colores: str, bot: bool, continuar: bool, sonidoActivado: bool, musicaActivado: bool):

        """Constructor de clase Juego."""
        if continuar:
            linea:str = open("registro/Registro de jugadas.txt","r").readline().split(" ")
            colores = linea[0]
            bot = linea[1]=="True"

        # Dimension del juego.
        self.AREA_JUEGO: PixelCoord = PixelCoord(x*0.63, x*0.63)

        # Dimension adicional necesaria para la GUI.
        self.AREA_ESTADO: PixelCoord = PixelCoord(x*0.36, 0)
        self.ORIGEN_JUEGO: PixelCoord = self.AREA_JUEGO/2
        self.hexagonoRadio: float = 35.5
        self.piezas = Piezas(colores)
        self.adaptador: HexPixelAdaptador = HexPixelAdaptador(self.AREA_JUEGO, self.ORIGEN_JUEGO, self.hexagonoRadio)
        self.bot = bot

        if bot:
            self.botNegro = Bot("n","Medio",self.adaptador, colores.endswith("n"))
            if colores.endswith("r"):

                self.botRojo = Bot("r","Medio",self.adaptador, True)

        self.continuar = continuar
        self.Musica = Musica("sonido/musica/")
        self.reproducir_sonidos = sonidoActivado
        self.reproducir_musica = musicaActivado
        self.Musica.iniciar(self.reproducir_musica)

    def iniciar(self, dificultad: str, pausa, juegoEjecutandose):
        Sonido().sonidoIniciarJuego(self.reproducir_sonidos)
        """Iniciar el juego."""
        # pygame.init()
        if self.bot:
            self.botNegro.dificultad = dificultad
            if self.piezas.colores.endswith("r"):
                self.botRojo.dificultad = dificultad

        # Dimension del juego.

        AREA_JUEGO = self.AREA_JUEGO
        
        # Dimension adicional necesaria para la GUI.
        AREA_ESTADO = self.AREA_ESTADO

        # Fuente de AREA_ESTADO


        FUENTE = pygame.font.Font("fnt/8-Bit.TTF", 10)

        FUENTE_MINUSCULA = pygame.font.SysFont("arialblack", 20)


        # Ancho y alto del juego.


        ANCHO_JUEGO, ALTO_JUEGO = AREA_JUEGO

        ANCHO_ESTADO = AREA_ESTADO[0]


        # Origen central del juego.
        ORIGEN_JUEGO = self.ORIGEN_JUEGO
        
        # Pantalla del juego.
        PANTALLA = pygame.display.get_surface()

        # Tablero de juego.
        HEX_TABLERO: Tablero = Tablero.generarMcCooey(self.piezas.colores)

        # El radio de un hexagono individual en pantalla, en pixeles.

        HEX_RADIO: self.hexagonoRadio

        # Lista de los colores de las celdas.
        HEX_COLORES: list[tuple] = [(60, 120, 60), (40, 40, 200), (184, 40, 50)]

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
        self.turnoJugador: int = 0  # Describe de quien es el turno (0: Blanco, 1: Negro, 2: Rojo).
        self.estadoRey: str = "" # Un mensaje sobre el estado de cualquiera de los reyes..
        self.turnoTexto: str = "" # Describe de quien es el turno (0: Blanco, 1: Negro, 2: Rojo).
    
        hexInicialBot: list(Optional[HexCoord], Optional[HexCoord]) = [None, None]  # The `HexCoord` of the start of the AI's move.
        hexFinalBot: list(Optional[HexCoord], Optional[HexCoord]) = [None, None]  # The `HexCoord` of the end of the AI's move.
        
        # Mensaje de qué lado es el turno.
        registroMovimientos = [] 
        sePuedeDeshacer = False


        # Lista de movimientos realizados por todos los jugadores.
        

        desplazamientoRegistro = 0


        desplazamientoArribaImg = Imagen("img/boton_Arriba.png")

        desplazamientoAbajoImg = Imagen("img/boton_Abajo.png")

        deshacerImg = Imagen("img/boton_Deshacer.png")


        botonDesplazamientoArriba = Boton(1030, 125, desplazamientoArribaImg.obtenerImagen())

        botonDesplazamientoAbajo = Boton(1030, 650, desplazamientoAbajoImg.obtenerImagen())

        botonDeshacer = Boton(10, 10, deshacerImg.obtenerImagen())


        @staticmethod
        def actualizarRegistro(movimiento, registro) -> bool:
            """Se actualiza el historial de movimientos con el movimiento que se pasa como parametro."""
            if movimiento != None:
                registro.append(movimiento)

            return len(registro) > 15

        def guardarJuego():
            """Cierra el programa y guarda el registro de jugadas en un archivo de texto."""
            archivo = open("registro/Registro de jugadas.txt","w")
            archivo.write(HEX_TABLERO.piezas.colores+" "+str(self.bot)+" "+str(HEX_TABLERO.turno)+"\n")
            for linea in registroMovimientos:
                archivo.write(linea+"\n")
            archivo.close()
            archivo = None
            archivo = open("registro/Estado tablero.txt","w")
            for celdaElegida in HEX_TABLERO:
                if celdaElegida.estado!=None:
                    archivo.write(celdaElegida.coordenada.__str__()+" "+str(celdaElegida.estado)+"\n")
            archivo.close()
            archivo = None

        def dibujaHex(coordenada: HexCoord, color: tuple, llenar=False):
            """Dibuja un hexagono en la pantalla."""
            pygame.draw.polygon(PANTALLA, color, ADAPTADOR.getVertices(
                coordenada), 0 if llenar else 3)

        def dibujarPiezas(celda: HexCelda, escala):
            """Dibuja una pieza en pantalla segun la celd ingresada."""
            pixelCoords: PixelCoord = ADAPTADOR.hexAPixel(celda.coordenada)
            if celda.estado is not None:
                if celda.coordenada == coordPiezaInicial:
                    return
                imagen = imagenesDePiezas[celda.estado]
                PANTALLA.blit(pygame.transform.scale(imagen, (imagen.get_width() * escala, imagen.get_height() * escala))
                    , pixelCoords - (AREA_PIEZA * escala))
                

        def evaluarEstadoDelRey():
            if HEX_TABLERO.elReyEstaEnJaque(HEX_TABLERO.piezas.colores[self.turnoJugador])!=None:
                if HEX_TABLERO.elReyEstaAhogado(HEX_TABLERO.piezas.colores[self.turnoJugador]):
                    # Se muestra en pantalla el mensaje de jaque mate
                    self.estadoRey = "Jaque Mate al Rey "+self.turnoTexto.replace(" ","")
                    mensajeDeEstadoDelRey(self, True)
                    
                else:
                    self.estadoRey = "Jaque al Rey "+self.turnoTexto.replace(" ","")
                    mensajeDeEstadoDelRey(self, False)
                
            elif HEX_TABLERO.elReyEstaAhogado(HEX_TABLERO.piezas.colores[self.turnoJugador]):
                self.estadoRey = "Rey "+self.turnoTexto.replace(" ","")+" ahogado"
                mensajeDeEstadoDelRey(self, True)
            
            else:
                self.estadoRey = ""
        
        def mensajeDeEstadoDelRey(self, mate: bool):
            """Dibuja una alerta que describe el estado de Jaque del rey del jugador actual."""
            # Previene al mensaje de aparecer al continuar el juego.
            if self.continuar:
                return
            # Si se hace un jaque al Bot no se muestra.
            if not mate and (self.bot) and (self.turnoJugador > 0):
                return
            
            # Si hay como mucho dos reyes y un rey se encuentra en jaque mate o ahogado, se finaliza el juego.
            esFin: bool = mate and HEX_TABLERO.contarReyes() <= 2

            botonTitulo: str = "Finalizar" if esFin else "Continuar"

            botonContinuar = Boton(350-FUENTE.render(botonTitulo, True, (255, 255, 255)).get_width()/2, 370, FUENTE.render(botonTitulo, True, (255, 255, 255)))


            ejecucion = True

            while ejecucion:

                pygame.draw.rect(PANTALLA, (0, 0, 0), (150, 280, 400, 150))

                text = FUENTE_MINUSCULA.render(self.estadoRey, True, (255, 255, 255))

                PANTALLA.blit(text, (350-text.get_width()/2, 330))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ejecucion = False
                        pygame.quit()
                        exit()
                  

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        mouse_pos = pygame.mouse.get_pos()

                        if botonContinuar.rectangulo.collidepoint(mouse_pos):

                            if esFin:

                                juegoEjecutandose[0] = False

                                if os.path.exists("registro/Estado tablero.txt"):

                                    os.remove("registro/Estado tablero.txt")

                            ejecucion = False
                        

                botonContinuar.dibujar()
                

                pygame.display.flip()     
                

        def actualizaElTurno():
            """Comprueba las jugadas realizadas y así determina de qué lado es el turno."""
            self.turnoJugador = HEX_TABLERO.turno % len(self.piezas.colores)
            self.turnoTexto = "Blanco" if self.turnoJugador == 0 else " Negro" if self.turnoJugador == 1 else "  Rojo" 
            if not HEX_TABLERO.elReyExiste(self.piezas.colores[self.turnoJugador]):

                if self.bot:

                    if  self.turnoJugador > 0:

                        if self.turnoJugador == 1: 

                            self.botNegro = None

                        else: 

                            self.botRojo = None

                    else:

                        self.estadoRey = "Fin del juego"

                        mensajeDeEstadoDelRey(self,True)


                HEX_TABLERO.turno += 1
                actualizaElTurno()
                self.continuar = False
                return
            evaluarEstadoDelRey()
            if HEX_TABLERO.elReyEstaAhogado(self.piezas.colores[self.turnoJugador]):
                HEX_TABLERO.turno += 1
                actualizaElTurno()
            self.continuar = False
                

        def escribeTexto(texto: str,tamanio: int, x: any, y: any, colorTexto):


            """ Genenera un texto en pantalla con la FUENTE y color de texto elegidos en la 
            posicion "x" e "y" de la pantalla con el texto elegido. """


            img = pygame.font.Font("fnt/8-Bit.TTF", tamanio).render(texto, True, colorTexto)

            PANTALLA.blit(img, (x, y) )  


        def continuarJuego():
            """Ejecuta las jugadas guardadas en el archivo de texto de registros para devolver el programa al estado en el que se lo dejó."""
            if os.path.exists("registro/Registro de jugadas.txt") and os.path.exists("registro/Estado tablero.txt"):
                archivo = open("registro/Registro de jugadas.txt","r")
                for linea in archivo.readlines():
                    palabras:str = linea.split(" ")
                    if len(palabras) < 4:
                        HEX_TABLERO.turno = int(palabras[2])
                        continue
                    else:
                        if actualizarRegistro(linea[:-1], registroMovimientos): desplazamientoRegistro = len(registroMovimientos) - 15
                archivo.close()
                for celdaElegida in HEX_TABLERO:
                    celdaElegida.estado = None
                archivo = open("registro/Estado tablero.txt","r")
                for linea in archivo.readlines():
                    palabras:str = linea.split(" ")
                    HEX_TABLERO.__setitem__(HexCoord(float(palabras[0][1:-1]),float(palabras[1][:-1]),float(palabras[2][:-1])), palabras[3][:-1])
                archivo.close()
                archivo = None

        if self.continuar: continuarJuego()
        actualizaElTurno()
        self.continuar = False


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
                    guardarJuego()
                    pygame.quit()
                    exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        guardarJuego()
                        pausa[0] = not pausa[0]
                        juegoEjecutandose[0] = False
                        
                if evento.type == pygame.MOUSEBUTTONUP:
                    # Traduce las coordenadas ingresadas a coordenadas axiales / hexagonales.
                    pixelSeleccionado: PixelCoord = PixelCoord(
                        *pygame.mouse.get_pos())
                    coordSeleccion: HexCoord = round(
                        ADAPTADOR.pixelAHex(pixelSeleccionado))
                    
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
                        if self.bot:
                            if not (self.turnoJugador == 0 and color == "b"):
                                continue
                        else:
                            if not ((self.turnoJugador == 0 and color == "b") or (self.turnoJugador == 1 and color == "n") or (self.turnoJugador == 2 and color == "r")):
                                continue
                        
                        Sonido().sonidoTomarPieza(self.reproducir_sonidos)
                        piezaSeleccionada = piezaEnHexagono
                        coordPiezaInicial = coordSeleccion
                        movimientosValidos = HEX_TABLERO.generarMovimientos(
                            coordPiezaInicial)

                    # De otro modo, se realizo clic con una pieza en mano.
                    else:
                        if coordSeleccion in movimientosValidos:
                            guardarJuego()

                            Sonido().sonidoSoltarPieza(self.reproducir_sonidos)

                            nuevoMov = HEX_TABLERO.moverPieza(
                                coordPiezaInicial, coordSeleccion, "jugador")
                            if actualizarRegistro(nuevoMov, registroMovimientos): desplazamientoRegistro = len(registroMovimientos) - 15
                            piezaSeleccionada = coordPiezaInicial = None
                            if nuevoMov != None:
                                actualizaElTurno()
                                sePuedeDeshacer = True
                            else: 
                                sePuedeDeshacer = False
            
            # se pone la pantalla de color blanco
            PANTALLA.fill((0, 0, 0))


            # se muestra la pantalla del juego con la imagen "Fondo_Juego.jpg"

            PANTALLA.blit(pygame.transform.scale(pygame.image.load(

                f"img/Fondo_Juego.png").convert_alpha(), (700, 710)), (0, 0))

            PANTALLA.blit(pygame.transform.scale(pygame.image.load(

                f"img/Fondo_Estado.png").convert_alpha(), (410, 710)), (700, 0))
            

            # Se dibuja la linea que va a separar el tablero con la interfaz de turnos.

            pygame.draw.line(PANTALLA, (62, 48, 92), (ANCHO_JUEGO+10, 0), (ANCHO_JUEGO+10, ALTO_JUEGO + 20), 15)
            

            # Dibuja los hexagonos de color.
            for celda in HEX_TABLERO:
                color: tuple[int, int, int] = HEX_COLORES[(
                    celda.coordenada.q - celda.coordenada.r) % 3]
                dibujaHex(celda.coordenada, color, llenar=True)
            
            # Pinta las celdas movidas por el Bot
            for i in range(2):
                if hexInicialBot[i] and hexFinalBot[i] is not None:
                    dibujaHex(hexInicialBot[i], (200, 100, 100), True)
            
            # Si se está haciendo jaque, se pinta la celda del atacante.
            if HEX_TABLERO.elReyEstaEnJaque(self.piezas.colores[self.turnoJugador])!=None:
                dibujaHex(HEX_TABLERO.elReyEstaEnJaque(self.piezas.colores[self.turnoJugador]), (255, 10, 10), llenar=True)
            
            # Dibuja los colores segun el estado del movimiento. Verde: movimientos posibles, Rojo: capturar piezas, Azul: celda actual.
            if dificultad != "Dificil":
                if coordPiezaInicial is not None:
                    for coord in movimientosValidos:
                        color: tuple[int, int, int] = (
                            255, 50, 50) if HEX_TABLERO[coord] else (50, 255, 50)
                        dibujaHex(coord, color, llenar=True)
                    dibujaHex(coordPiezaInicial, (50, 50, 255), llenar=True)
            
            # Dibuja el borde negro de los hexagonos y dibuja las piezas.
            for celda in HEX_TABLERO:
                dibujaHex(celda.coordenada, (20, 20, 20))
                dibujarPiezas(celda, 1)
            
            # Si estamos sosteniendo una pieza se dibuja en la posicion del mouse.
            if piezaSeleccionada:
                imagen = imagenesDePiezas[piezaSeleccionada]
                PANTALLA.blit(pygame.transform.scale(imagen, (imagen.get_width() * 1, imagen.get_height() * 1))
                    , pygame.mouse.get_pos())
            
            # Dibuja los movimientos guardados en el registro
            for i in range(15):
                if 0 <= (i + desplazamientoRegistro) < len(registroMovimientos):

                    escribeTexto(registroMovimientos[i + desplazamientoRegistro], 15 , (ANCHO_JUEGO + 30) , (145 + i * 35), (255,255,255))


            if botonDesplazamientoArriba.dibujar():

                if desplazamientoRegistro > 0: 
                            desplazamientoRegistro -= 1
            

            if botonDesplazamientoAbajo.dibujar():

                desplazamientoRegistro += 1
            
            # Posibilidad de deshacer una jugada, solo para el modo facil.
            if dificultad == "Facil" and sePuedeDeshacer and piezaSeleccionada==None:
                if botonDeshacer.dibujar():
                    registroMovimientos = []
                    HEX_TABLERO.turno -= 1
                    continuarJuego()
                    actualizaElTurno()
                    sePuedeDeshacer = False
            
            # Describe de quien es el turno:


            escribeTexto("Turno del jugador", 20, (ANCHO_JUEGO+55), 38,(255,255,255))

            escribeTexto(self.turnoTexto, 20, (ANCHO_JUEGO+165), 64,(255,255,255))


            # Describe el estado de Jaque:


            escribeTexto(self.estadoRey, 15, (ANCHO_JUEGO+10+len(self.estadoRey)), 95,(255,255,255))
            

            # Actualiza la pantalla.
            pygame.display.flip()
            
            # Realiza los movimientos de un Bot.
            if self.turnoJugador > 0 and self.bot:
                # Se designa el bot al que le toca jugar.
                bot = self.botNegro if self.turnoJugador == 1 else self.botRojo
                

                pygame.draw.rect(PANTALLA, (0, 0, 0), (150, 280, 400, 150))

                textoJugador = FUENTE_MINUSCULA.render("El jugador "+("Negro" if self.turnoJugador == 1 else "Rojo") , True, (255, 255, 255))

                PANTALLA.blit(textoJugador, (350-textoJugador.get_width()/2, 350-textoJugador.get_height()))

                texto = FUENTE_MINUSCULA.render("está jugando, espere por favor..." , True, (255, 255, 255))

                PANTALLA.blit(texto, (350-texto.get_width()/2, 380-texto.get_height()))

                pygame.display.flip()

                movimiento = bot.mover(HEX_TABLERO)
                

                if movimiento != None:

                    Sonido().sonidoSoltarPieza(self.reproducir_sonidos)

                    (hexInicialBot[self.turnoJugador-1], hexFinalBot[self.turnoJugador-1]), nuevoMov = movimiento
                    if actualizarRegistro(nuevoMov, registroMovimientos): desplazamientoRegistro = len(registroMovimientos) - 15
                
                actualizaElTurno()
                
