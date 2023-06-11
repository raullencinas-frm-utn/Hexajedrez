import os
from typing import Optional
import pygame

from boton import Boton
from imagen import Imagen
from juego import Juego
from metodos import Metodos
from tablero import Tablero
from sonido import Sonido

pygame.init()

# Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 710

# Se define el tamanio de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

# Titulo de la pantalla
pygame.display.set_caption("HEXajedrez")

# Se define el icono
icono = Imagen("img/hex_icono.png")
# Se dibuja el icono
pygame.display.set_icon(icono.obtenerImagen())

# Se define la tipografia
FUENTE = pygame.font.Font("fnt/8-Bit.TTF", 30)
# Se define el color de las letras
BLANCO = (255, 255, 255)

# Variables del menu
opcionesDeJuego = False
pantallaDePausa = [False]
juegoEjecutandose = [True]
pantallaDeOpciones = False
pantallaDificultad = False
pantallaCreditos = False

# Opciones:
opciones = [False, "Medio", True, True]
"""Bot, dificultad, sonido, musica."""

def comoJugar():
    y = ALTO_PANTALLA/2
    x = ANCHO_PANTALLA/2
    esFin = False
    comoJugar = {
        0: {
            "imagen": "img/como/p_inicio.png",
            "descripcion": "Esta pantalla te da la bienvenida y te invita a sumergirte en una emocionante partida de Hexajedrez. Al presiona la tecla de espacio podrás explorar distintas modalidades de juego."
        },
        1: {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Luego de presionar espacio se presentan diferentes opciones para que el jugador elija la modalidad que prefiera:"
        },
        2: {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra uno: En este modo podrás desafiar a otro jugador en una partida de hexajedrez. Puedes disfrutar de partidas amistosas o competir estratégicamente con amigos o familiares."
        },
        3: {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra dos: Este modo te permitirá poner a prueba tus habilidades enfrentándote a dos oponentes controlados por jugadores. Excelente opción si deseas un desafío adicional o si quieres practicar tus estrategias enfrentando multiples adversarios."
        },
        4: {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra CPU: En esta modalidad podrás enfrentarte a una computadora controlada por el juego que te desafiará en el Hexajedrez ideal para entrenar y mejorar tus estrategias asi como perfeccionar tus movimientos."
        },
        5: {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra dos CPUs: En este modo tendrás la oportunidad de enfrentarte a multiples oponentes controlados por la computadora, lo cual te brindará una experiencia desafiante y emocionante."
        },
        6: {
            "imagen": "img/como/p_juego.png",
            "descripcion": "El tablero de juego tiene una forma hexagonal única, y está compuesto por 91 hexagonos en total con 6 hexágonos en cada lado que pueden variar en 3 colores diferentes."
        },
        7: {
            "imagen": "img/como/p_1vs1.png",
            "descripcion": "En el modo uno contra uno los jugadores utilizan dos colores de piezas blancas y negras. Cada jugador cuenta con 7 peones, 2 caballos, 2 torres, 3 alfiles, la dama, y por último el rey."
        },
        8: {
            "imagen": "img/como/p_1vs2.png",
            "descripcion": "En el modo uno contra dos oponentes las piezas se encuentran ubicadas en 3 de los vértices enfrentados del tablero hexagonal. Se agregan las piezas de color rojo para representar al tercer jugador."
        },
        9: {
            "imagen": "img/como/p_1vs2.png",
            "descripcion": "Esta variante de juego con 3 jugadores suma un nuevo nivel de complejidad y estrategia ya que los jugadores deberan considerar las interacciones con dos oponentes."
        },

        10: {
            "imagen": "img/como/m_peon.png",
            "descripcion": "En la siguientes imágenes se muestran los movimientos correspondientes a las piezas del Hexajedrez comenzando con el peón:"
        },

        11: {
            "imagen": "img/como/m_peon.png",
            "descripcion": "Al igual que en el ajedrez convencional, los peones se desplazan hacia adelante en el tablero hexagonal."
        },

        12: {
            "imagen": "img/como/m_peon.png",
            "descripcion": "Cuando se encuentra en su posición inicial tiene la opción de avanzar dos hexágonos hacia adelante en lugar de uno. Esto le brinda la posibilidad de realizar un avance estratégico desde el inicio del juego."
        },


        13: {
            "imagen": "img/como/m_peon2.png",
            "descripcion": "Sin embargo si el peon ya se ha movido de su posicion inicial solo puede avanzar un hexágono hacia adelante en cada turno."
        },

        14: {
            "imagen": "img/como/m_peon2.png",
            "descripcion": "Ademas el peón tiene la capacidad de capturar las piezas en los hexagonos adyacentes en sentido diagonal. Esto significa que puede eliminar las piezas en las posiciones diagonales hacia adelante a su izquierda o derecha."
        },


        15: {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre puede moverse verticalmente horizontalmente o en diagonal dentro de los hexágonos adyacentes que comparten lados con su posición actual."
        },

        16: {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre puede avanzar o retroceder en estas direcciones rectas siempre y cuando no haya obstáculos en su camino."
        },

        17: {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre no puede saltar sobre otras piezas. Si hay una pieza bloqueando el camino de la torre no podrá pasar mas allá de esa posición."
        },

        18: {
            "imagen": "img/como/m_torre.png",
            "descripcion": "Aprovecha la movilidad de la torre en el tablero hexagonal para controlar filas y columnas atacar a las piezas enemigas y establecer una defensa sólida."
        },

        19: {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre es una pieza valiosa en Hexajedrez y su correcto uso puede marcar la diferencia en el desarrollo de la partida."
        },
        20: {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "El alfil puede moverse a traves de los hexagonos que comparten los vértices del hexágono actual permitiendo un movimiento en diagonal y horizontal."
        },

        21: {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Es importante tener en cuenta que no puede saltar sobre otras piezas y su movimiento está limitado a los hexágonos en el camino de los vertices."
        },

        22: {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Utiliza al alfil de manera inteligente para atacar desde diferentes angulos controlar areas clave del tablero y desplegar una estrategia efectiva en Hexajedrez."
        },

        23: {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Su combinación de movimientos diagonal y horizontal lo convierte en una pieza valiosa para dominar el juego."
        },

        24: {
            "imagen": "img/como/m_dama.png",
            "descripcion": "La dama puede moverse verticalmente, horizontalmente, y en diagonal a traves de los hexagonos adyacentes. Su alcance abarca todas las direcciones posibles en el tablero."
        },

        25: {
            "imagen": "img/como/m_dama.png",
            "descripcion": "Al igual que las piezas anteriores, la dama no puede saltar sobre otras piezas y su movimiento está limitado a los hexágonos disponibles en su camino."
        },

        26: {
            "imagen": "img/como/m_dama.png",
            "descripcion": "La versatilidad y amplitud de movimiento de la dama la convierten en una pieza poderosa en Hexajedrez."
        },

        27: {
            "imagen": "img/como/m_dama.png",
            "descripcion": "Puede atacar desde diversas direcciones, controlar múltiples areas del tablero y ser un factor determinante en el desarrollo del juego. Aprovecha al máximo las capacidades estratégicas de la dama para obtener ventaja sobre tus oponentes en Hexajedrez."
        },

        28: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El rey tiene la capacidad de moverse en todas las direcciones pero se limita a moverse solo un hexágono por turno."
        },


        29: {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "El caballo se mueve en dirección a los vertices de los hexágonos. Su movimiento especial consiste en trasladarse al hexágono que comparte lado con el hexágono que comparte vértice con el hexágono de partida"
        },

        30: {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "Puede moverse en cualquier dirección hacia estos hexágonos saltando sobre otras piezas en el proceso."
        },

        31: {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "Aprovecha esta capacidad unica de los caballos en Hexajedrez para sorprender a tus oponentes, crear amenazas estratégicas, y aprovechar las oportunidades tácticas."
        },

        32: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El rey puede desplazarse verticalmente horizontalmente y en diagonal a través de los hexágonos adyacentes siempre avanzando un solo paso a la vez."
        },

        33: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Su rango de movimiento es más limitado en comparación con la dama pero sigue siendo esencial para la supervivencia y estrategia del juego."
        },

        34: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El objetivo principal del juego es poner al rey en una posición de jaque mate por lo que debes asegurarte de mantenerlo seguro y evitar amenazas directas. Si el rey es capturado, la partida se pierde."
        },

        35: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Utiliza al rey de manera inteligente para protegerlo y buscar oportunidades estratégicas. Mueve al rey con precaucion evaluando el entorno y considerando las amenazas potenciales"
        },

        36: {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Recuerda que la seguridad del rey es fundamental para alcanzar la victoria en Hexajedrez."
        },


        37: {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En este panel se muestra información relevante sobre el estado actual del juego."
        },

        38: {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En la parte superior del panel se encuentra un mensaje que indica de qué jugador es el turno. Esto es útil para tener claridad sobre quién debe tomar su jugada en cada momento."
        },

        39: {
            "imagen": "img/como/p_estado.png",
            "descripcion": "El panel notifica si el rey esta en jaque o jaque mate. Esto es importante para saber si el rey de un jugador está en una posicion amenazada por una pieza enemiga o si el rey ha sido capturado."
        },

        40: {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En el panel lateral también se muestra una lista con los movimientos realizados durante la partida. Esto permite tener un registro de todas las jugadas que se han llevado a cabo."
        },

        41: {
            "imagen": "img/como/p_estado.png",
            "descripcion": "Finalmente el panel lateral cuenta con botones que permiten desplazarnos por la vista de los movimientos. Estos botones facilitan la navegación entre los movimientos, lo que brinda la posibilidad de revisar y repasar las jugadas realizadas en cualquier momento."},

        42: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "El menú de pausa en Hexajedrez. Este menú se puede acceder en cualquier momento durante el juego al presionar la tecla de escape. El menú de pausa ofrece varias opciones para el jugador incluyendo:"
        },

        43: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Continuar: Al seleccionar esta opción, el juego se reanuda desde el punto en el que fue pausado y se regresa a la pantalla de juego activa."
        },
        44: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Opciones: Al seleccionar esta opción se abre un submenú que permite al jugador personalizar diferentes configuraciones del juego como la dificultad, el sonido y la música."
        },
        45: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Como Jugar: Al seleccionar esta opción se muestra una pantalla con las instrucciones y reglas básicas del juego proporcionando orientación adicional sobre como jugar Hexajedrez."
        },
        46: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Créditos: Al seleccionar esta opción se muestra una pantalla que reconoce a los integrantes y detalles del proyecto."
        },
        47: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Menú Principal: Al seleccionar esta opción se regresa al menú principal del juego, dónde se pueden realizar otras acciones como iniciar una nueva partida o seleccionar un modo de juego diferente."
        },
        48: {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Salir: Al seleccionar esta opción se sale completamente del juego y se cierra la aplicación."
        },
        49: {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "En la siguiente imágen se muestra el menú de opciones en Hexajedrez. Este menú ofrece diferentes configuraciones y ajustes que el jugador puede modificar según sus preferencias. Las opciones disponibles en el menú de opciones incluyen:"
        },
        50: {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Dificultad: Permite al jugador seleccionar el nivel de dificultad del juego. Esto determinará el nivel de desafío que enfrentará el jugador al enfrentarse a la computadora. Las opciones de dificultad pueden variar de fácil, medio, o difícil. Los invitamos a descubrir las funciones propias de cada modo."
        },
        51: {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Sonido: Permite al jugador activar o desactivar los efectos de sonido del juego. Al activar el sonido se reproducirán efectos de sonido relacionados con las acciones del juego como movimientos de piezas o selección. Al desactivar el sonido, el juego se jugará sin efectos de sonido."
        },
        52: {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Música: Permite al jugador activar o desactivar la música de fondo del juego. Si se activa la música se reproducirá una melodía de fondo durante la partida lo que puede agregar ambiente al juego. Si se desactiva la música el juego se jugará sin musica de fondo."
        },
        53: {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Volver: Al seleccionar esta opción el jugador regresará al menú de pausa donde se pueden realizar otros ajustes o continuar con el juego"
        },
        54: {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Al iniciar el juego después de una interrupción o cierre previo se muestra el mensaje: Hay una partida guardada, Presiona la tecla Espacio para continuar o la tecla N para comenzar una nueva partida. El jugador tiene dos opciones disponibles:"
        },

        55: {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Presionar la tecla Espacio: Esto permitirá al jugador retomar la partida guardada desde el punto en que se interrumpió. El juego se cargará y el jugador podrá continuar jugando desde ese punto."
        },

        56: {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Presionar la tecla N: Si el jugador desea comenzar una nueva partida en lugar de continuar la partida guardada se seleccionará esta opción. Al hacerlo se accederá al menú de selección de modo de juego."
        }
    }
    ejecucion = True
    botonTitulo: str = "Finalizar"
    botonFinalizar = Boton(30, 650, pygame.font.Font("fnt/8-Bit.TTF", 20).render(
                botonTitulo, True, (255, 255, 255)))
    for i in range(57):

        info = comoJugar[i]
        pantalla.blit(pygame.transform.scale(pygame.image.load(
            f"img/Fondo_Naranja.jpg").convert_alpha(), (1100, 715)), (0, -2.5))
        pantalla.blit(Imagen(info["imagen"]).obtenerImagen(), (x - (Imagen(info["imagen"]).obtenerImagen(
        ).get_width()/2), (y-(Imagen(info["imagen"]).obtenerImagen().get_height()/2))))
        botonTitulo: str = "Finalizar" if esFin else "Continuar"
        botonContinuar = Boton(900, 650, pygame.font.Font("fnt/8-Bit.TTF", 20).render(
            botonTitulo, True, (255, 255, 255)))
        
        pantalla.blit(
            Imagen("img/HEXajedrez.png").obtenerImagen(), (310, 10))
        Metodos.dibujarCuadroTexto(info["descripcion"], 750, 150)
        siguiente = True
        while siguiente:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if botonContinuar.rectangulo.collidepoint(mouse_pos):
                        if i == 55:
                            esFin = True
                        siguiente = False
                    if botonFinalizar.rectangulo.collidepoint(mouse_pos):
                        siguiente = False
                        i = 58

                        
                if not esFin:        
                    botonContinuar.dibujar()
                botonFinalizar.dibujar()
                pygame.display.flip()
        if i > 57: break
        
        creditosDesplazamiento: int = 0  

# Imagenes del Menu
unoContraUnoImg = Imagen("img/boton_uno_contra_uno.png")
unoContraDosImg = Imagen("img/boton_uno_contra_dos.png")
unoContraCpuImg = Imagen("img/boton_uno_contra_cpu.png")
unoContraDosCpuImg = Imagen("img/boton_uno_contra_dos_cpu.png")
activadoImg = Imagen("img/caja_activado.png")
desactivadoImg = Imagen("img/caja_desactivado.png")

# Titulo menu
hexajedrezImg = Imagen("img/HEXajedrez.png")

# Imagen de fondo
fondoRojoImg = Imagen('img/Fondo_Rojo.png')
fondoAmarilloImg = Imagen('img/Fondo_Amarillo.png')
fondoCelesteImg = Imagen('img/Fondo_Celeste.png')
fondoVerdeImg = Imagen('img/Fondo_Verde.jpg')
fondoNaranjaImg = Imagen('img/Fondo_Naranja.jpg')

# Metodos
metodo = Metodos()

# Crear Botones
botonUnoContraUno = Boton(0, 285, unoContraUnoImg.obtenerImagen())
botonUnoContraDos = Boton(0, 385, unoContraDosImg.obtenerImagen())
botonUnoContraCpu = Boton(0, 485, unoContraCpuImg.obtenerImagen())
botonUnoContraDosCpu = Boton(0, 585, unoContraDosCpuImg.obtenerImagen())
botonContinuar = Boton(0, 210, FUENTE.render("Continuar", True, BLANCO))
botonOpciones = Boton(0, 260, FUENTE.render("Opciones", True, BLANCO))
botonComoJugar = Boton(0, 310, FUENTE.render("Como jugar", True, BLANCO))
botonCreditos = Boton(0, 360, FUENTE.render("Creditos", True, BLANCO))
botonMenuPrincipal = Boton(0, 410, FUENTE.render("Menu principal", True, BLANCO))
botonSalir = Boton(0, 460, FUENTE.render("Salir", True, BLANCO))
botonSonido = Boton(495, 395, FUENTE.render("Sonido", True, BLANCO))
botonMusica = Boton(500, 345, FUENTE.render("Musica", True, BLANCO))
botonSonidoCheckBox = Boton(660, 395, desactivadoImg.obtenerImagen())
botonMusicaCheckBox = Boton(660, 345, desactivadoImg.obtenerImagen())
botonDificultad = Boton(0, 295, FUENTE.render("Dificultad", True, BLANCO))
botonFacil = Boton(280, 295, FUENTE.render("Facil", True, BLANCO))
botonMedio = Boton(0, 295, FUENTE.render("Medio", True, BLANCO))
botonDificil = Boton(820, 295, FUENTE.render("Dificil", True, BLANCO))
botonVolver = Boton(0, 245, FUENTE.render("Volver", True, BLANCO))

# Bucle de ejecucion
ejecucion = True
num_canales_originales = 0
pygame.mixer.music.load("sonido/8-bit-dream-land-142093.mp3")
pygame.mixer.music.play(-1)
while ejecucion:
    # Pintar la pantalla de color blanco
    pantalla.fill(BLANCO)
    if not opciones[3]:
        pygame.mixer.music.set_volume(0.0)
    else:
        pygame.mixer.music.set_volume(0.75)  

    # PANTALLA DE PAUSA
    
    if pantallaDePausa[0] == True:
        if pantallaCreditos:
            creditosDesplazamiento = metodo.creditos(creditosDesplazamiento)
            # PANTALLA DE OPCIONES
            
        elif pantallaDeOpciones:
            
            # se muestra el fondo verde con los botones de opciones
            
            fondoVerdeImg.dibujar(0, 0)

            # se muestran las opciones de musica y sonido asi como sus cajitas de opciones.

            if botonSonido.dibujar() or botonSonidoCheckBox.dibujar():
                opciones[2] = not opciones[2]
                Sonido.volumen = opciones[2]

            if botonMusica.dibujar() or botonMusicaCheckBox.dibujar():
                opciones[3] = not opciones[3]

            activadoImg.dibujar(660, 395) if opciones[2] else desactivadoImg.dibujar(660, 395)
            activadoImg.dibujar(660, 345) if opciones[3] else desactivadoImg.dibujar(660, 345)

            if pantallaDificultad:
                if botonFacil.dibujar():
                    opciones[1] = "Facil"
                    pantallaDificultad = False
                if botonMedio.dibujar():
                    opciones[1] = "Medio"
                    pantallaDificultad = False
                if botonDificil.dibujar():
                    opciones[1] = "Dificil"
                    pantallaDificultad = False
            else:
                if botonDificultad.dibujar():
                    pantallaDificultad = True

            if botonVolver.dibujar():

                # Se abandona la pantalla de opciones

                pantallaDeOpciones = False

        else:

            # se muestra el fondo celeste y se dibujan los botones

            fondoCelesteImg.dibujar(0, 0)

            # se chequea que boton se presiona y se abre la ventana correspondiente

            if botonContinuar.dibujar():
                pantallaDePausa[0] = False

            if botonOpciones.dibujar():
                # Abre la pantalla de opciones
                pantallaDeOpciones = True

            if botonComoJugar.dibujar():
                # Se muestran las instrucciones de como jugar.
                comoJugar()
                pantallaDePausa[0] = False
                
            if botonCreditos.dibujar():
                creditosDesplazamiento = 600
                metodo.creditos(creditosDesplazamiento)
                pantallaCreditos = True

            if botonMenuPrincipal.dibujar():
                
                # Se vuelve el programa al menu inicial
                
                juegoEjecutandose[0] = False
                opcionesDeJuego = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sonido/8-bit-dream-land-142093.mp3")
                pygame.mixer.music.play(-1)
                                
                pantallaDePausa[0] = False

            if botonSalir.dibujar():

                # Se abandona el bucle de ejecucion y cierra el programa

                ejecucion = False

    # PANTALLA DE MODOS DE JUEGO

    elif opcionesDeJuego == True:
        # Se selecciona el fondo mediante un condicional
        
        # Se continua el juego si existe una partida.
        if os.path.exists("registro/Registro de jugadas.txt") and os.path.exists("registro/Estado tablero.txt") :
            archivo = open("registro/Registro de jugadas.txt","r")
            if len(archivo.readlines())>1:
                juegoEjecutandose[0] = True
                Juego(ANCHO_PANTALLA, "", opciones[0], True, opciones[2], opciones[3]).iniciar(opciones[1], pantallaDePausa, juegoEjecutandose)

            archivo.close()
            archivo = None
            
        # Se dibuja el fondo amarillo

        fondoAmarilloImg.dibujar(0, 0)

        # Se muestra el titulo

        hexajedrezImg.dibujar(0, 120)

        # Se dibujan los botones de los modos de juego y al presionarlos cambia la pantalla

        if botonUnoContraUno.dibujar():
            juegoEjecutandose[0] = True
            Juego(ANCHO_PANTALLA, "bn",opciones[0], False, opciones[2], opciones[3]).iniciar(opciones[1], pantallaDePausa, juegoEjecutandose)
        if botonUnoContraDos.dibujar():
            juegoEjecutandose[0] = True
            Juego(ANCHO_PANTALLA, "bnr",opciones[0], False, opciones[2], opciones[3]).iniciar(opciones[1], pantallaDePausa, juegoEjecutandose)
        if botonUnoContraCpu.dibujar():
            juegoEjecutandose[0] = True
            Juego(ANCHO_PANTALLA, "bn", True, False, opciones[2], opciones[3]).iniciar(opciones[1], pantallaDePausa, juegoEjecutandose)
        if botonUnoContraDosCpu.dibujar():
            juegoEjecutandose[0] = True
            Juego(ANCHO_PANTALLA, "bnr", True, False, opciones[2], opciones[3]).iniciar(opciones[1], pantallaDePausa, juegoEjecutandose)
    

    # PANTALLA DE TITULO

    else:

        # se dibuja el fondo rojo

        fondoRojoImg.dibujar(0, 0)
        
        hexajedrezImg.dibujar(0, ALTO_PANTALLA/2)

        # se dibuja el texto en la pantalla
        if os.path.exists("registro/Registro de jugadas.txt") and len(open("registro/Registro de jugadas.txt","r").readlines())>1 and os.path.exists("registro/Estado tablero.txt"):
            Metodos.dibujarTexto("Hay una partida guardada", 30, (255, 255, 70), 0, 490)
            Metodos.dibujarTexto("Presione ESPACIO para continuar", 20, BLANCO, 0, 540)
            Metodos.dibujarTexto("o N para comenzar nuevo juego", 20, BLANCO, 0, 580)
        else:
            Metodos.dibujarTexto("Presione ESPACIO para comenzar", 30, BLANCO, 0, 500)
            Metodos.dibujarTexto("o ESCAPE para mas opciones", 20, BLANCO, 0, 550)
    # Escucha eventos

    for evento in pygame.event.get():

        # si se presiona el boton de cierre se termina el bucle

        if evento.type == pygame.QUIT:
            ejecucion = False

        # actualizar la ventana al redimensionar

        elif evento.type == pygame.KEYDOWN:

            # si la tecla presionada es espacio

            if evento.key == pygame.K_SPACE:
                opcionesDeJuego = True

            # si se presiona la tecla escape

            if evento.key == pygame.K_ESCAPE:
                juegoEjecutandose[0] = not juegoEjecutandose[0]
                pantallaDePausa[0] = not pantallaDePausa[0]
                pantallaDeOpciones = False
                pantallaDificultad = False
                pantallaCreditos = False
            if evento.key == pygame.K_n:
                if os.path.exists("registro/Registro de jugadas.txt"):
                    os.remove("registro/Registro de jugadas.txt")
                if os.path.exists("registro/Estado tablero.txt"):
                    os.remove("registro/Estado tablero.txt")
                opcionesDeJuego = True

    # Actualiza la pantalla

    pygame.display.update()

# Cierra el programa

pygame.quit()
