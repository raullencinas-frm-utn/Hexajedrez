import pygame
from boton import Boton
from time import sleep

pygame.init()

# Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 700

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))


# Titulo de la pantall
pygame.display.set_caption("HEXajedrez")

icono = pygame.image.load("img/hex_icon.png")
pygame.display.set_icon(icono)

# se define la tipografia
fuente = pygame.font.SysFont("arialblack", 40)
# se define el color de las letras
COLOR_LETRAS = (255, 255, 255)

# variables menu
opcionesDeJuego = False

# Imagenes del Menu
unoContraUnoImg = pygame.image.load("img/boton_uno_contra_uno.png").convert_alpha()
unoContraDosImg = pygame.image.load("img/boton_uno_contra_dos.png").convert_alpha()
unoContraCpuImg = pygame.image.load("img/boton_uno_contra_cpu.png").convert_alpha()
unoContraDosCpuImg = pygame.image.load(
    "img/boton_uno_contra_dos_cpu.png"
).convert_alpha()

# titulo menu
hexajedrezImg = pygame.image.load("img/HEXajedrez.png").convert_alpha()

# Imagen de fondo
fondoRojoImg = pygame.transform.scale(
    pygame.image.load("img/Back_Red.png").convert_alpha(),
    (ANCHO_PANTALLA, ALTO_PANTALLA),
)
fondoAmarilloImg = pygame.transform.scale(
    pygame.image.load("img/Back_Amarillo.png").convert_alpha(),
    (ANCHO_PANTALLA, ALTO_PANTALLA),
)

# Crear Botones
botonUnoContraUno = Boton(304, 245, unoContraUnoImg, 1)
botonUnoContraDos = Boton(304, 345, unoContraDosImg, 1)
botonUnoContraCpu = Boton(304, 445, unoContraCpuImg, 1)
botonUnoContraDosCpu = Boton(304, 545, unoContraDosCpuImg, 1)


# Funciones
def dibujaTexto(texto, fuente, colorTexto, x, y):
    img = fuente.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))


# bucle del juego
ejecucion = True
while ejecucion:
    pantalla.fill((52, 78, 91))
    if opcionesDeJuego == True:
        pantalla.blit(fondoAmarilloImg, (0, 0))
        pantalla.blit(hexajedrezImg, (100, 20))
        if botonUnoContraUno.dibujar(pantalla):
            print("inicia juego 1 contra 1")
        if botonUnoContraDos.dibujar(pantalla):
            print("inicia juego 1 contra 2")
        if botonUnoContraCpu.dibujar(pantalla):
            print("inicia juego 1 contra CPU")
        if botonUnoContraDosCpu.dibujar(pantalla):
            print("inicia juego 1 contra 2 CPU")
    else:
        pantalla.blit(fondoRojoImg, (0, 0))
        # se dibuja el texto en la pantalla
        dibujaTexto("Presione espacio para comenzar", fuente, COLOR_LETRAS, 200, 500)

    # Escucha eventos
    for evento in pygame.event.get():
        # si se aprieta una tecla se valida que
        if evento.type == pygame.KEYDOWN:
            # si la tecla presionada es espacio
            if evento.key == pygame.K_SPACE:
                opcionesDeJuego = True
        # si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
            ejecucion = False
    pygame.display.update()
pygame.quit()
# sleep(3)#Prueba para ver la ventana funcionar
