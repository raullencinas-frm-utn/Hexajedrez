import os
from typing import Optional
import pygame
from boton import Boton
from imagen import Imagen
from juego import Juego
from tablero import Tablero

pygame.init()

# Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 700

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
"""IA, dificultad, sonido, musica."""

# Funciones


def dibujaTexto(texto, tamanio, colorTexto, x, y, posicion: Optional[str]):
    """ Genenera un texto en pantalla con la FUENTE y color de texto elegidos en la 
    posicion "x" e "y" de la pantalla con el texto elegido. """
    img = pygame.font.Font(
        "fnt/8-Bit.TTF", tamanio).render(texto, True, colorTexto)
    if posicion == "Centrado":
        anchoPantalla, altoPantalla = pygame.display.get_window_size()
        x = (anchoPantalla/2) - (img.get_width()/2)
    pantalla.blit(img, (x, y))


def draw_text_box(text, width, height):
    y = 700-height
    x = 1100
    WHITE = (255, 255, 255)
    fuenteTam = 25
    fuente = pygame.font.SysFont(None, fuenteTam)
    lines = []
    words = text.split(" ")
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        if fuente.size(test_line)[0] <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    y += (height - len(lines) * (fuenteTam + 2.5)) // 2

    for line in lines:
        text_surface = fuente.render(line, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x // 2
        text_rect.y = y
        pygame.draw.rect(pantalla, (0, 0, 0), ((text_rect.x-2.5),
                         (y-2.5), (text_rect.width+5), (text_rect.height+5)))
        pantalla.blit(text_surface, text_rect)
        y += fuenteTam + 5


def comoJugar():
    y = ALTO_PANTALLA/2
    x = ANCHO_PANTALLA/2
    esFin = False
    pagina = 0
    comoJugar = {
        "inicio": {
            "imagen": "img/como/p_inicio.png",
            "descripcion": "Esta pantalla te da la bienvenida y te invita a sumergirte en una emocionante partida de Hexajedrez. Al presiona la tecla de espacio podrás explorar distintas modalidades de juego."
        },
        "seleccion1": {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Luego de presionar espacio se presentan diferentes opciones para que el jugador elija la modalidad que prefiera:"
        },
        "seleccion2": {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra uno: En este modo podrás desafiar a otro jugador en una partida de hexajedrez. Puedes disfrutar de partidas amistosas o competir estratégicamente con amigos o familiares."
        },
        "seleccion3": {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra dos: Este modo te permitirá poner a prueba tus habilidades enfrentándote a dos oponentes controlados por jugadores. Excelente opción si deseas un desafío adicional o si quieres practicar tus estrategias enfrentando multiples adversarios."
        },
        "seleccion4": {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra CPU: En esta modalidad podrás enfrentarte a una computadora controlada por el juego que te desafiará en el Hexajedrez ideal para entrenar y mejorar tus estrategias asi como perfeccionar tus movimientos."
        },
        "seleccion5": {
            "imagen": "img/como/p_seleccion.png",
            "descripcion": "Uno contra dos CPUs: En este modo tendrás la oportunidad de enfrentarte a multiples oponentes controlados por la computadora, lo cual te brindará una experiencia desafiante y emocionante."
        },
        "juego": {
            "imagen": "img/como/p_juego.png",
            "descripcion": "El tablero de juego tiene una forma hexagonal única, y está compuesto por 91 hexagonos en total con 6 hexágonos en cada lado que pueden variar en 3 colores diferentes."
        },
        "1vs1": {
            "imagen": "img/como/p_1vs1.png",
            "descripcion": "En el modo uno contra uno los jugadores utilizan dos colores de piezas blancas y negras. Cada jugador cuenta con 7 peones, 2 caballos, 2 torres, 3 alfiles, la dama, y por último el rey."
        },
        "1vs2": {
            "imagen": "img/como/p_1vs2.png",
            "descripcion": "En el modo uno contra dos oponentes las piezas se encuentran ubicadas en 3 de los vértices enfrentados del tablero hexagonal. Se agregan las piezas de color rojo para representar al tercer jugador."
        },
        "1vs2a": {
            "imagen": "img/como/p_1vs2.png",
            "descripcion": "Esta variante de juego con 3 jugadores suma un nuevo nivel de complejidad y estrategia ya que los jugadores deberan considerar las interacciones con dos oponentes."
        },

        "peon": {
            "imagen": "img/como/m_peon.png",
            "descripcion": "En la siguientes imágenes se muestran los movimientos correspondientes a las piezas del Hexajedrez comenzando con el peón:"
        },

        "peon1": {
            "imagen": "img/como/m_peon.png",
            "descripcion": "Al igual que en el ajedrez convencional, los peones se desplazan hacia adelante en el tablero hexagonal."
        },

        "peon1.1": {
            "imagen": "img/como/m_peon.png",
            "descripcion": "Cuando se encuentra en su posición inicial tiene la opción de avanzar dos hexágonos hacia adelante en lugar de uno. Esto le brinda la posibilidad de realizar un avance estratégico desde el inicio del juego."
        },


        "peon2": {
            "imagen": "img/como/m_peon2.png",
            "descripcion": "Sin embargo si el peon ya se ha movido de su posicion inicial solo puede avanzar un hexágono hacia adelante en cada turno."
        },

        "peon2.1": {
            "imagen": "img/como/m_peon2.png",
            "descripcion": "Ademas el peón tiene la capacidad de capturar las piezas en los hexagonos adyacentes en sentido diagonal. Esto significa que puede eliminar las piezas en las posiciones diagonales hacia adelante a su izquierda o derecha."
        },


        "torre": {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre puede moverse verticalmente horizontalmente o en diagonal dentro de los hexágonos adyacentes que comparten lados con su posición actual."
        },

        "torre1": {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre puede avanzar o retroceder en estas direcciones rectas siempre y cuando no haya obstáculos en su camino."
        },

        "torre2": {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre no puede saltar sobre otras piezas. Si hay una pieza bloqueando el camino de la torre no podrá pasar mas allá de esa posición."
        },

        "torre3": {
            "imagen": "img/como/m_torre.png",
            "descripcion": "Aprovecha la movilidad de la torre en el tablero hexagonal para controlar filas y columnas atacar a las piezas enemigas y establecer una defensa sólida."
        },

        "torre4": {
            "imagen": "img/como/m_torre.png",
            "descripcion": "La torre es una pieza valiosa en Hexajedrez y su correcto uso puede marcar la diferencia en el desarrollo de la partida."
        },
        "alfil": {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "El alfil puede moverse a traves de los hexagonos que comparten los vértices del hexágono actual permitiendo un movimiento en diagonal y horizontal."
        },

        "alfil1": {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Es importante tener en cuenta que no puede saltar sobre otras piezas y su movimiento está limitado a los hexágonos en el camino de los vertices."
        },

        "alfil2": {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Utiliza al alfil de manera inteligente para atacar desde diferentes angulos controlar areas clave del tablero y desplegar una estrategia efectiva en Hexajedrez."
        },

        "alfil2": {
            "imagen": "img/como/m_alfil.png",
            "descripcion": "Su combinación de movimientos diagonal y horizontal lo convierte en una pieza valiosa para dominar el juego."
        },

        "dama": {
            "imagen": "img/como/m_dama.png",
            "descripcion": "La dama puede moverse verticalmente, horizontalmente, y en diagonal a traves de los hexagonos adyacentes. Su alcance abarca todas las direcciones posibles en el tablero."
        },

        "dama1": {
            "imagen": "img/como/m_dama.png",
            "descripcion": "Al igual que las piezas anteriores, la dama no puede saltar sobre otras piezas y su movimiento está limitado a los hexágonos disponibles en su camino."
        },

        "dama2": {
            "imagen": "img/como/m_dama.png",
            "descripcion": "La versatilidad y amplitud de movimiento de la dama la convierten en una pieza poderosa en Hexajedrez."
        },

        "dama3": {
            "imagen": "img/como/m_dama.png",
            "descripcion": "Puede atacar desde diversas direcciones, controlar múltiples areas del tablero y ser un factor determinante en el desarrollo del juego. Aprovecha al máximo las capacidades estratégicas de la dama para obtener ventaja sobre tus oponentes en Hexajedrez."
        },

        "rey": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El rey tiene la capacidad de moverse en todas las direcciones pero se limita a moverse solo un hexágono por turno."
        },


        "caballo": {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "El caballo se mueve en dirección a los vertices de los hexágonos. Su movimiento especial consiste en trasladarse al hexágono que comparte lado con el hexágono que comparte vértice con el hexágono de partida"
        },

        "caballo1": {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "Puede moverse en cualquier dirección hacia estos hexágonos saltando sobre otras piezas en el proceso."
        },

        "caballo2": {
            "imagen": "img/como/m_caballo.png",
            "descripcion": "Aprovecha esta capacidad unica de los caballos en Hexajedrez para sorprender a tus oponentes, crear amenazas estratégicas, y aprovechar las oportunidades tácticas."
        },

        "rey1": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El rey puede desplazarse verticalmente horizontalmente y en diagonal a través de los hexágonos adyacentes siempre avanzando un solo paso a la vez."
        },

        "rey2": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Su rango de movimiento es más limitado en comparación con la dama pero sigue siendo esencial para la supervivencia y estrategia del juego."
        },

        "rey3": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "El objetivo principal del juego es poner al rey en una posición de jaque mate por lo que debes asegurarte de mantenerlo seguro y evitar amenazas directas. Si el rey es capturado, la partida se pierde."
        },

        "rey4": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Utiliza al rey de manera inteligente para protegerlo y buscar oportunidades estratégicas. Mueve al rey con precaucion evaluando el entorno y considerando las amenazas potenciales"
        },

        "rey5": {
            "imagen": "img/como/m_rey.png",
            "descripcion": "Recuerda que la seguridad del rey es fundamental para alcanzar la victoria en Hexajedrez."
        },


        "estado": {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En este panel se muestra información relevante sobre el estado actual del juego."
        },

        "estado1": {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En la parte superior del panel se encuentra un mensaje que indica de qué jugador es el turno. Esto es útil para tener claridad sobre quién debe tomar su jugada en cada momento."
        },

        "estado2": {
            "imagen": "img/como/p_estado.png",
            "descripcion": "El panel notifica si el rey esta en jaque o jaque mate. Esto es importante para saber si el rey de un jugador está en una posicion amenazada por una pieza enemiga o si el rey ha sido capturado."
        },

        "estado3": {
            "imagen": "img/como/p_estado.png",
            "descripcion": "En el panel lateral también se muestra una lista con los movimientos realizados durante la partida. Esto permite tener un registro de todas las jugadas que se han llevado a cabo."
        },

        "estado4": {
            "imagen": "img/como/p_estado.png",
            "descripcion": "Finalmente el panel lateral cuenta con botones que permiten desplazarnos por la vista de los movimientos. Estos botones facilitan la navegación entre los movimientos, lo que brinda la posibilidad de revisar y repasar las jugadas realizadas en cualquier momento."},

        "pausa": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "El menú de pausa en Hexajedrez. Este menú se puede acceder en cualquier momento durante el juego al presionar la tecla de escape. El menú de pausa ofrece varias opciones para el jugador incluyendo:"
        },

        "pausa1": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Continuar: Al seleccionar esta opción, el juego se reanuda desde el punto en el que fue pausado y se regresa a la pantalla de juego activa."
        },
        "pausa2": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Opciones: Al seleccionar esta opción se abre un submenú que permite al jugador personalizar diferentes configuraciones del juego como la dificultad, el sonido y la música."
        },
        "pausa3": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Como Jugar: Al seleccionar esta opción se muestra una pantalla con las instrucciones y reglas básicas del juego proporcionando orientación adicional sobre como jugar Hexajedrez."
        },
        "pausa4": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Créditos: Al seleccionar esta opción se muestra una pantalla que reconoce a los integrantes y detalles del proyecto."
        },
        "pausa5": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Menú Principal: Al seleccionar esta opción se regresa al menú principal del juego, dónde se pueden realizar otras acciones como iniciar una nueva partida o seleccionar un modo de juego diferente."
        },
        "pausa6": {
            "imagen": "img/como/p_pausa.png",
            "descripcion": "Salir: Al seleccionar esta opción se sale completamente del juego y se cierra la aplicación."
        },
        "opciones": {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "En la siguiente imágen se muestra el menú de opciones en Hexajedrez. Este menú ofrece diferentes configuraciones y ajustes que el jugador puede modificar según sus preferencias. Las opciones disponibles en el menú de opciones incluyen:"
        },
        "opciones1": {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Dificultad: Permite al jugador seleccionar el nivel de dificultad del juego. Esto determinará el nivel de desafío que enfrentará el jugador al enfrentarse a la computadora. Las opciones de dificultad pueden variar de fácil, medio, o difícil. Los invitamos a descubrir las funciones propias de cada modo."
        },
        "opciones2": {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Sonido: Permite al jugador activar o desactivar los efectos de sonido del juego. Al activar el sonido se reproducirán efectos de sonido relacionados con las acciones del juego como movimientos de piezas o selección. Al desactivar el sonido, el juego se jugará sin efectos de sonido."
        },
        "opciones3": {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Música: Permite al jugador activar o desactivar la música de fondo del juego. Si se activa la música se reproducirá una melodía de fondo durante la partida lo que puede agregar ambiente al juego. Si se desactiva la música el juego se jugará sin musica de fondo."
        },
        "opciones4": {
            "imagen": "img/como/p_opciones.png",
            "descripcion": "Volver: Al seleccionar esta opción el jugador regresará al menú de pausa donde se pueden realizar otros ajustes o continuar con el juego"
        },
        "guardado": {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Al iniciar el juego después de una interrupción o cierre previo se muestra el mensaje: Hay una partida guardada, Presiona la tecla Espacio para continuar o la tecla N para comenzar una nueva partida. El jugador tiene dos opciones disponibles:"
        },

        "guardado1": {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Presionar la tecla Espacio: Esto permitirá al jugador retomar la partida guardada desde el punto en que se interrumpió. El juego se cargará y el jugador podrá continuar jugando desde ese punto."
        },

        "guardado2": {
            "imagen": "img/como/p_guardado.png",
            "descripcion": "Presionar la tecla N: Si el jugador desea comenzar una nueva partida en lugar de continuar la partida guardada se seleccionará esta opción. Al hacerlo se accederá al menú de selección de modo de juego."
        }
    }
    running = True
    while running:
        for ayuda, info in comoJugar.items():
            pantalla.blit(pygame.transform.scale(pygame.image.load(
                f"img/Fondo_Naranja.jpg").convert_alpha(), (1100, 715)), (0, -2.5))
            pantalla.blit(Imagen(info["imagen"]).obtenerImagen(), (x - (Imagen(info["imagen"]).obtenerImagen(
            ).get_width()/2), (y-(Imagen(info["imagen"]).obtenerImagen().get_height()/2))))
            botonTitulo: str = "Finalizar" if esFin else "Continuar"
            botonContinuar = Boton(840, 650, FUENTE.render(
                botonTitulo, True, (255, 255, 255)), .9)
            pantalla.blit(
                Imagen("img/HEXajedrez.png").redimensionar(500, 125), (310, 10))
            draw_text_box(info["descripcion"], 750, 150)
            siguiente = True
            while siguiente:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if botonContinuar.rectangulo.collidepoint(mouse_pos):

                            if (pagina == 54):
                                esFin = True
                            siguiente = False
                            pagina += 1
                    botonContinuar.dibujar("")
                    pygame.display.flip()
        comoJugar = None
        running = False


creditosDesplazamiento: int = 0  # te quiero lea! <3


def creditos(creditosDesplazamiento):
    creditosDesplazamiento -= .5
    pantalla.blit(fondoCelesteImg.redimensionar(
        ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
    # Se dibujan los creditos en pantalla
    pantalla.blit(hexajedrezImg.obtenerImagen(),
                  (120, -80+creditosDesplazamiento))
    dibujaTexto("Un programa de ajedrez hexagonal ", 20, BLANCO,
                0, 130+creditosDesplazamiento, "Centrado")
    dibujaTexto("realizado en Python", 20, BLANCO, 0,
                160+creditosDesplazamiento, "Centrado")
    dibujaTexto("En este trabajo presentamos el", 20, BLANCO,
                0, 190+creditosDesplazamiento, "Centrado")
    dibujaTexto("desarrollo de un juego de computadora ", 20,
                BLANCO, 0, 220+creditosDesplazamiento, "Centrado")
    dibujaTexto("llamado HEXajedrez que simula", 20, BLANCO,
                0, 250+creditosDesplazamiento, "Centrado")
    dibujaTexto("el Ajedrez Hexagonal de mesa que es ", 20,
                BLANCO, 0, 280+creditosDesplazamiento, "Centrado")
    dibujaTexto("una variante del famoso juego", 20, BLANCO,
                0, 310+creditosDesplazamiento, "Centrado")
    dibujaTexto("Ajedrez que se juega en un tablero", 20, BLANCO,
                0, 340+creditosDesplazamiento, "Centrado")
    dibujaTexto("de celdas hexagonales en lugar de cuadradas", 20,
                BLANCO, 0, 370+creditosDesplazamiento, "Centrado")
    dibujaTexto("El objetivo consiste en programar este juego", 20,
                BLANCO, 0, 400+creditosDesplazamiento, "Centrado")
    dibujaTexto("en Python sin conocimientos previos", 20,
                BLANCO, 0, 430+creditosDesplazamiento, "Centrado")

    dibujaTexto("Integrantes", 30, BLANCO, 0, 500 +
                creditosDesplazamiento, "Centrado")
    dibujaTexto("Espejo Mezzabotta Giuliano", 15, BLANCO,
                0, 540+creditosDesplazamiento, "Centrado")
    dibujaTexto("Lencinas Berenguer Raul Alejandro", 15, BLANCO,
                0, 570+creditosDesplazamiento, "Centrado")
    dibujaTexto("Maureira Ezequiel Jesus", 15, BLANCO, 0,
                600+creditosDesplazamiento, "Centrado")
    dibujaTexto("Santilli Elias Vicente", 15, BLANCO, 0,
                630+creditosDesplazamiento, "Centrado")
    dibujaTexto("Valdearenas Leandro Javier", 15, BLANCO,
                0, 660+creditosDesplazamiento, "Centrado")
    dibujaTexto("Varberde Thompson Francisco Alejandro", 15,
                BLANCO, 0, 690+creditosDesplazamiento, "Centrado")
    dibujaTexto("Detalles", 30, BLANCO, 0, 740 +
                creditosDesplazamiento, "Centrado")
    dibujaTexto("Docente Ing Carlos Rodriguez", 15, BLANCO,
                0, 790+creditosDesplazamiento, "Centrado")
    dibujaTexto("Metodologia de la Investigacion", 15, BLANCO,
                0, 820+creditosDesplazamiento, "Centrado")
    dibujaTexto("Universidad Tecnologica Nacional", 15, BLANCO,
                0, 850+creditosDesplazamiento, "Centrado")
    dibujaTexto("( Facultad Regional de Mendoza )", 15, BLANCO,
                0, 880+creditosDesplazamiento, "Centrado")

    if creditosDesplazamiento < -900:
        # Se abandona la pantalla de creditos
        creditosDesplazamiento = 0
        pantallaCreditos = False

    return creditosDesplazamiento


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

# Crear Botones
botonUnoContraUno = Boton(0, 245, unoContraUnoImg.obtenerImagen(), 1)
botonUnoContraDos = Boton(0, 345, unoContraDosImg.obtenerImagen(), 1)
botonUnoContraCpu = Boton(0, 445, unoContraCpuImg.obtenerImagen(), 1)
botonUnoContraDosCpu = Boton(0, 545, unoContraDosCpuImg.obtenerImagen(), 1)
botonContinuar = Boton(0, 245, FUENTE.render("Continuar", True, BLANCO), 1)
botonOpciones = Boton(0, 295, FUENTE.render("Opciones", True, BLANCO), 1)
botonComoJugar = Boton(0, 345, FUENTE.render("Como jugar", True, BLANCO), 1)
botonCreditos = Boton(0, 395, FUENTE.render("Creditos", True, BLANCO), 1)
botonMenuPrincipal = Boton(0, 410, FUENTE.render(
    "Menu principal", True, BLANCO), 1)
botonSalir = Boton(0, 445, FUENTE.render("Salir", True, BLANCO), 1)
botonSonido = Boton(0, 245, FUENTE.render("Sonido", True, BLANCO), 1)
botonMusica = Boton(0, 295, FUENTE.render("Musica", True, BLANCO), 1)
botonSonidoCheckBox = Boton(660, 245, desactivadoImg.obtenerImagen(), 1)
botonMusicaCheckBox = Boton(660, 295, desactivadoImg.obtenerImagen(), 1)
botonDificultad = Boton(0, 345, FUENTE.render("Dificultad", True, BLANCO), 1)
botonFacil = Boton(280, 345, FUENTE.render("Facil", True, BLANCO), 1)
botonMedio = Boton(0, 345, FUENTE.render("Medio", True, BLANCO), 1)
botonDificil = Boton(680, 345, FUENTE.render("Dificil", True, BLANCO), 1)
botonVolver = Boton(0, 395, FUENTE.render("Volver", True, BLANCO), 1)

# Bucle de ejecucion
ejecucion = True
while ejecucion:
    # Pintar la pantalla de color blanco
    pantalla.fill(BLANCO)

    # PANTALLA DE PAUSA
    if pantallaDePausa[0] == True:
        if pantallaCreditos:
            creditosDesplazamiento = creditos(creditosDesplazamiento)
            # PANTALLA DE OPCIONES
        elif pantallaDeOpciones:
            # se muestra el fondo verde con los botones de opciones
            pantalla.blit(fondoVerdeImg.redimensionar(
                ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))

            # se muestran las opciones de musica y sonido asi como sus cajitas de opciones.
            if botonSonido.dibujar("Centrado") or botonSonidoCheckBox.dibujar(""):
                opciones[2] = not opciones[2]
            if botonMusica.dibujar("Centrado") or botonMusicaCheckBox.dibujar(""):
                opciones[3] = not opciones[3]
            pantalla.blit(activadoImg.obtenerImagen(
            ) if opciones[2] else desactivadoImg.obtenerImagen(), (660, 245))
            pantalla.blit(activadoImg.obtenerImagen(
            ) if opciones[3] else desactivadoImg.obtenerImagen(), (660, 295))

            if pantallaDificultad:
                if botonFacil.dibujar(""):
                    opciones[1] = "Facil"
                    pantallaDificultad = False
                if botonMedio.dibujar("Centrado"):
                    opciones[1] = "Medio"
                    pantallaDificultad = False
                if botonDificil.dibujar(""):
                    opciones[1] = "Dificil"
                    pantallaDificultad = False
            else:
                if botonDificultad.dibujar("Centrado"):
                    pantallaDificultad = True

            if botonVolver.dibujar("Centrado"):
                # Se abandona la pantalla de opciones
                pantallaDeOpciones = False

        else:
            # se muestra el fondo celeste y se dibujan los botones
            pantalla.blit(fondoCelesteImg.redimensionar(
                ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))

            # se chequea que boton se presiona y se abre la ventana correspondiente
            if botonContinuar.dibujar("Centrado"):
                pantallaDePausa[0] = False

            if botonOpciones.dibujar("Centrado"):
                # Abre la pantalla de opciones
                pantallaDeOpciones = True

            if botonComoJugar.dibujar("Centrado"):
                # Se muestran las instrucciones de como jugar.
                comoJugar()
                pantallaDePausa[0] = False

            if botonCreditos.dibujar("Centrado"):
                creditos(creditosDesplazamiento)
                creditosDesplazamiento = 600
                pantallaCreditos = True

            if botonMenuPrincipal.dibujar("Centrado"):
                # Se vuelve el programa al menu inicial
                juegoEjecutandose[0] = False
                opcionesDeJuego = False
                pantallaDePausa[0] = False

            if botonSalir.dibujar("Centrado"):
                # Se abandona el bucle de ejecucion y cierra el programa
                ejecucion = False

    # PANTALLA DE MODOS DE JUEGO
    elif opcionesDeJuego == True:
        # Se selecciona el fondo mediante un condicional

        # Se dibuja el fondo amarillo
        pantalla.blit(fondoAmarilloImg.redimensionar(
            ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
        # Se muestra el titulo
        pantalla.blit(hexajedrezImg.obtenerImagen(), (100, 20))
        # Se dibujan los botones de los modos de juego y al presionarlos cambia la pantalla
        if botonUnoContraUno.dibujar("Centrado"):
            Juego(ANCHO_PANTALLA, "bn").iniciar()
        if botonUnoContraDos.dibujar("Centrado"):
            pantallaAzul = True
            print("inicia juego 1 contra 2")
        if botonUnoContraCpu.dibujar("Centrado"):
            pantallaAzul = True
            print("inicia juego 1 contra CPU")
        if botonUnoContraDosCpu.dibujar("Centrado"):
            pantallaAzul = True
            print("inicia juego 1 contra 2 CPU")

    # PANTALLA DE TITULO
    else:
        # se dibuja el fondo rojo
        pantalla.blit(fondoRojoImg.redimensionar(
            ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
        # se dibuja el texto en la pantalla
        dibujaTexto("Presione ESPACIO para comenzar",
                    30, BLANCO, 130, 500, None)
        dibujaTexto("o ESCAPE para mas opciones", 20, BLANCO, 295, 550, None)

    # Escucha eventos
    for evento in pygame.event.get():

        # si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
            ejecucion = False

        # actualizar la ventana al redimensionar
        elif evento.type == pygame.VIDEORESIZE:
            # Obtener las nuevas dimensiones de la pantalla
            ANCHO_PANTALLA, ALTO_PANTALLA = evento.w, evento.h

            # Calcular la relacion de aspecto actual
            relacion_de_aspecto = ANCHO_PANTALLA / ALTO_PANTALLA

            # Redimensionar la pantalla manteniendo la relacion de aspecto
            pantalla = pygame.display.set_mode((ANCHO_PANTALLA, int(
                ANCHO_PANTALLA / relacion_de_aspecto)), pygame.RESIZABLE)

            # Actualizar la pantalla
            pygame.display.flip()

        # si se aprieta una tecla se valida que
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
    # Actualiza la pantalla
    pygame.display.update()
# Cierra el programa
pygame.quit()
