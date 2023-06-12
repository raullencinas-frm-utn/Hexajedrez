import pygame
from boton import Boton

from imagen import Imagen

class Metodos:
    def __init__(self) -> None:
        self.fondoNaranjaImg = Imagen('img/Fondo_Naranja.jpg')
        self.hexajedrezCreditosImg = Imagen("img/HEXajedrez-creditos.png")
        self.botonFinalizarComoJugar = Boton(100, 680, pygame.font.Font("fnt/8-Bit.TTF", 20).render("Finalizar", True, (255, 255, 255)))
        self.botonContinuarComoJugar = Boton(1000, 680, pygame.font.Font("fnt/8-Bit.TTF", 20).render("Continuar", True, (255, 255, 255)))
        self.fondoCelesteImg = Imagen('img/Fondo_Celeste.png')

    def dibujarTexto(texto, tamanio, colorTexto, x, y):
        """ Genenera un texto en pantalla con la FUENTE y color de texto elegidos en la 
        posicion "x" e "y" de la pantalla con el texto elegido. """
        anchoPantalla, altoPantalla = pygame.display.get_window_size()
        escala_x = anchoPantalla / 1100
        escala_y = altoPantalla / 700
        if escala_x > escala_y:
            escala = escala_y
        else:
            escala = escala_x
        
        imagen = pygame.font.Font("fnt/8-Bit.TTF", int(tamanio)).render(texto, True, colorTexto)
        ancho = imagen.get_width()
        alto = imagen.get_height()
        rectangulo = imagen.get_rect()
        if x != 0: 
            x-= 1100/2
        y-= 700/2
        
        nueva_y = altoPantalla/2 - (alto * escala)/2 + y * escala
        nueva_x = anchoPantalla/2 - (ancho * escala)/2 + x * escala
        rectangulo[1] = rectangulo[1] * escala 
        rectangulo[0] = rectangulo[0] * escala
        rectangulo.topleft = (nueva_x,nueva_y)
        pygame.display.get_surface().blit(pygame.transform.scale(imagen, (ancho * escala, alto * escala)), (nueva_x,nueva_y))

    def dibujarCuadroTexto(texto, ancho, alto):
        """Dibuja lineas de texto con fondo negro."""
        anchoPantalla, altoPantalla = pygame.display.get_window_size()
        escala_x = anchoPantalla / 1100
        escala_y = altoPantalla / 700
        
        if escala_x > escala_y:
            escala = escala_y
        else:
            escala = escala_x
        
        ancho = ancho * escala
        alto = alto * escala
        y = altoPantalla-alto
        x = anchoPantalla
        WHITE = (255, 255, 255)
        fuenteTam = int(19 * escala)
        espacio = 3
        fuente = pygame.font.SysFont("arialblack", fuenteTam)
        lineas = []
        palabras = texto.split(" ")
        lineaActual = palabras[0]
        for palabra in palabras[1:]:
            test_line = lineaActual + " " + palabra
            if fuente.size(test_line)[0] <= ancho:
                lineaActual = test_line
            else:
                lineas.append(lineaActual)
                lineaActual = palabra

        lineas.append(lineaActual)

        y += (alto - len(lineas) * (fuenteTam + 2.5)) // 2
        espacio = espacio * escala
        pantalla = pygame.display.get_surface()

        for linea in lineas:
            textoSuperficie = fuente.render(linea, True, WHITE)
            textoRectangulo = textoSuperficie.get_rect()
            textoRectangulo.centerx = x // 2
            textoRectangulo.y = y
            
            pygame.draw.rect(pantalla, (0, 0, 0), ((textoRectangulo.x-espacio),
                            (y-espacio), (textoRectangulo.width+(espacio*2)), (textoRectangulo.height+(espacio*2))))
            pantalla.blit(textoSuperficie, textoRectangulo)
            y += fuenteTam + fuenteTam/2

    def comoJugar(self):
        """Muestra un menu con las instrucciones del juego."""
        anchoPantalla, altoPantalla = pygame.display.get_window_size()
        
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
        

        for i in range(57):
            siguiente = True
            
            while siguiente:
                anchoPantalla, altoPantalla = pygame.display.get_surface().get_size()
                escala_x = anchoPantalla / 1100
                escala_y = altoPantalla / 700
                if escala_x > escala_y:
                    escala = escala_y
                else:
                    escala = escala_x
                
                pygame.display.get_surface().fill((0,0,0))
                info = comoJugar[i]
                self.fondoNaranjaImg.dibujar(0,0)
                imagen = Imagen(info["imagen"]).obtenerImagen()
                pygame.display.get_surface().blit(pygame.transform.scale(
                    imagen, (imagen.get_width() * escala, imagen.get_height() * escala)),
                    (anchoPantalla/2 - imagen.get_width() * escala *.5, altoPantalla/2 -imagen.get_height() * escala * .5))

                self.hexajedrezCreditosImg.dibujar(0,60)
                
                Metodos.dibujarCuadroTexto(info["descripcion"], 800, 170)

                if not esFin:
                    if self.botonContinuarComoJugar.dibujar():
                        if i == 55:
                            esFin = True
                        siguiente = False
                if self.botonFinalizarComoJugar.dibujar():
                    siguiente = False
                    i = 58
        
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
                pygame.display.flip()

            if i >= 56:
                break
                    
    def creditos(self, creditosDesplazamiento):
        """Dibuja y desplaza los creditos a lo alto de la pantalla."""
        creditosDesplazamiento -= 2
        self.fondoCelesteImg.dibujar(0, 0)
        BLANCO = (255,255,255)

        # Se dibujan los creditos en pantalla
        self.hexajedrezCreditosImg.dibujar(0, 40+creditosDesplazamiento)
        Metodos.dibujarTexto("Un programa de ajedrez hexagonal ", 20, BLANCO,
                    0, 130+creditosDesplazamiento)
        Metodos.dibujarTexto("realizado en Python", 20, BLANCO, 0,
                    160+creditosDesplazamiento)
        Metodos.dibujarTexto("En este trabajo presentamos el", 20, BLANCO,
                    0, 190+creditosDesplazamiento)
        Metodos.dibujarTexto("desarrollo de un juego de computadora ", 20,
                    BLANCO, 0, 220+creditosDesplazamiento)
        Metodos.dibujarTexto("llamado HEXajedrez que simula", 20, BLANCO,
                    0, 250+creditosDesplazamiento)
        Metodos.dibujarTexto("el Ajedrez Hexagonal de mesa que es ", 20,
                    BLANCO, 0, 280+creditosDesplazamiento)
        Metodos.dibujarTexto("una variante del famoso juego", 20, BLANCO,
                    0, 310+creditosDesplazamiento)
        Metodos.dibujarTexto("Ajedrez que se juega en un tablero", 20, BLANCO,
                    0, 340+creditosDesplazamiento)
        Metodos.dibujarTexto("de celdas hexagonales en lugar de cuadradas", 20,
                    BLANCO, 0, 370+creditosDesplazamiento)
        Metodos.dibujarTexto("El objetivo consiste en programar este juego", 20,
                    BLANCO, 0, 400+creditosDesplazamiento)
        Metodos.dibujarTexto("en Python sin conocimientos previos", 20,
                    BLANCO, 0, 430+creditosDesplazamiento)

        Metodos.dibujarTexto("Integrantes", 30, BLANCO, 0, 500 +
                    creditosDesplazamiento)
        Metodos.dibujarTexto("Espejo Mezzabotta Giuliano", 15, BLANCO,
                    0, 540+creditosDesplazamiento)
        Metodos.dibujarTexto("Lencinas Berenguer Raul Alejandro", 15, BLANCO,
                    0, 570+creditosDesplazamiento)
        Metodos.dibujarTexto("Maureira Ezequiel Jesus", 15, BLANCO, 0,
                    600+creditosDesplazamiento)
        Metodos.dibujarTexto("Santilli Elias Vicente", 15, BLANCO, 0,
                    630+creditosDesplazamiento)
        Metodos.dibujarTexto("Valdearenas Leandro Javier", 15, BLANCO,
                    0, 660+creditosDesplazamiento)
        Metodos.dibujarTexto("Varberde Thompson Francisco Alejandro", 15,
                    BLANCO, 0, 690+creditosDesplazamiento)
        Metodos.dibujarTexto("Detalles", 30, BLANCO, 0, 740 +
                    creditosDesplazamiento)
        Metodos.dibujarTexto("Docente Ing Carlos Rodriguez", 15, BLANCO,
                    0, 790+creditosDesplazamiento)
        Metodos.dibujarTexto("Metodologia de la Investigacion", 15, BLANCO,
                    0, 820+creditosDesplazamiento)
        Metodos.dibujarTexto("Universidad Tecnologica Nacional", 15, BLANCO,
                    0, 850+creditosDesplazamiento)
        Metodos.dibujarTexto("( Facultad Regional de Mendoza )", 15, BLANCO,
                    0, 880+creditosDesplazamiento)

        return creditosDesplazamiento