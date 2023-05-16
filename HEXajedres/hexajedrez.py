import pygame
from boton import Boton
from time import sleep

pygame.init()

# Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 700

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA),pygame.RESIZABLE)


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
pantallaDePausa = False

# Funciones
def dibujaTexto(texto, fuente, colorTexto, x, y):
    img = fuente.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))
    
def cargar_imagen(rutaImagen):
    imagen = pygame.image.load(rutaImagen)
    anchoImagen = ANCHO_PANTALLA
    relacionAspecto = imagen.get_width() / imagen.get_height()
    altoImagen = int(anchoImagen / relacionAspecto)
    x = 0
    y = int(ALTO_PANTALLA / 2 - altoImagen / 2)
    imagenEscalada = pygame.transform.scale(imagen, (anchoImagen, altoImagen))
    return imagenEscalada

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
fondoRojoImg = cargar_imagen("img/Back_Red.png")
fondoAmarilloImg = cargar_imagen("img/Back_Amarillo.png")

# Crear Botones
botonUnoContraUno = Boton(304, 245, unoContraUnoImg, 1)
botonUnoContraDos = Boton(304, 345, unoContraDosImg, 1)
botonUnoContraCpu = Boton(304, 445, unoContraCpuImg, 1)
botonUnoContraDosCpu = Boton(304, 545, unoContraDosCpuImg, 1)
botonContinuar = Boton(304,245,pygame.font.SysFont("arialblack", 40).render("Continuar", True, (255,255,255)),1)
botonOpciones = Boton(304,295,pygame.font.SysFont("arialblack", 40).render("Opciones", True, (255,255,255)),1)
botonComoJugar = Boton(304,345,pygame.font.SysFont("arialblack", 40).render("Como jugar", True, (255,255,255)),1)
botonCreditos = Boton(304,395,pygame.font.SysFont("arialblack", 40).render("Creditos", True, (255,255,255)),1)
botonSalir = Boton(304,445,pygame.font.SysFont("arialblack", 40).render("Salir", True, (255,255,255)),1)

# bucle del juego
ejecucion = True
while ejecucion:
    pantalla.fill((52, 78, 91))
    if pantallaDePausa == True:
        pantalla.fill((50,50,50,128))
        if botonContinuar.dibujar(pantalla):
            print("Continuar")
        if botonOpciones.dibujar(pantalla):
            print("Opciones")
        if botonComoJugar.dibujar(pantalla):
            print("Como Jugar") 
        if botonCreditos.dibujar(pantalla):
            print("Creditos") 
        if botonSalir.dibujar(pantalla):
            print("Salir")  
    elif opcionesDeJuego == True:
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
        
        # si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
             ejecucion = False
        elif evento.type == pygame.VIDEORESIZE:
            ANCHO_PANTALLA, ALTO_PANTALLA = evento.size
            pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.RESIZABLE)
        # si se aprieta una tecla se valida que
        elif evento.type == pygame.KEYDOWN:
            # si la tecla presionada es espacio
            if evento.key == pygame.K_SPACE:
                opcionesDeJuego = True
            if evento.key == pygame.K_ESCAPE:
                pantallaDePausa = not pantallaDePausa
        
    pygame.display.update()
pygame.quit()
# sleep(3)#Prueba para ver la ventana funcionar
