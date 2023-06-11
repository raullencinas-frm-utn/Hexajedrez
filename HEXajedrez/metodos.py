import pygame
from boton import Boton

from imagen import Imagen

class Metodos:
    def __init__(self) -> None:
        self.hexajedrezCreditosImg = Imagen("img/HEXajedrez-creditos.png")
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
                    
    def creditos(self, creditosDesplazamiento):
        """Dibuja y desplaza los creditos a lo alto de la pantalla."""
        creditosDesplazamiento -= 1
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