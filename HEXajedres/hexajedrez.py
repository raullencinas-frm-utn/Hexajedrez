import pygame
from boton import Boton
from time import sleep

pygame.init()

# Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 700

#Se define el tamanio de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))


# Titulo de la pantall
pygame.display.set_caption("HEXajedrez")

#se define el icono
icono = pygame.image.load("img/hex_icono.png")
#se utiliza el icono
pygame.display.set_icon(icono)

# se define la tipografia
fuente = pygame.font.SysFont("arialblack", 40)
# se define el color de las letras
COLOR_LETRAS = (255, 255, 255)

# variables menu
opcionesDeJuego = False
pantallaDePausa = False
pantallaDeOpciones = False
pantallaAzul = False

# Funciones
def dibujaTexto(texto, fuente, colorTexto, x, y):
    """La funcion dibujaTexto tiene como parametros
       (texto, fuente, colorTexto, x ,y)
       Lo que hace es genenerar un texto en pantalla 
       con la fuente y color de texto elegidos en la 
       posicion "x" e "y" de la pantalla con el texto 
       elegido.
    """
    img = fuente.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))



# Imagenes del Menu
unoContraUnoImg = pygame.image.load("img/boton_uno_contra_uno.png").convert_alpha()
unoContraDosImg = pygame.image.load("img/boton_uno_contra_dos.png").convert_alpha()
unoContraCpuImg = pygame.image.load("img/boton_uno_contra_cpu.png").convert_alpha()
unoContraDosCpuImg = pygame.image.load("img/boton_uno_contra_dos_cpu.png").convert_alpha()

# titulo menu
hexajedrezImg = pygame.image.load("img/HEXajedrez.png").convert_alpha()


# Imagen de fondo
fondoRojoImg = pygame.transform.scale(pygame.image.load('img/Fondo_Rojo.png').convert_alpha(),(ANCHO_PANTALLA, ALTO_PANTALLA))
fondoAmarilloImg = pygame.transform.scale(pygame.image.load('img/Fondo_Amarillo.png').convert_alpha(),(ANCHO_PANTALLA, ALTO_PANTALLA))
fondoCelesteImg = pygame.transform.scale(pygame.image.load('img/Fondo_Celeste.png').convert_alpha(),(ANCHO_PANTALLA,ALTO_PANTALLA))
fondoVerdeImg = pygame.transform.scale(pygame.image.load('img/Fondo_Verde.jpg').convert_alpha(),(ANCHO_PANTALLA,ALTO_PANTALLA)) 
pantallaAzulImg = pygame.transform.scale(pygame.image.load('img/pantallaAzul.png').convert_alpha(),(ANCHO_PANTALLA, ALTO_PANTALLA))

# Crear Botones
botonUnoContraUno = Boton(304, 245, unoContraUnoImg, 1)
botonUnoContraDos = Boton(304, 345, unoContraDosImg, 1)
botonUnoContraCpu = Boton(304, 445, unoContraCpuImg, 1)
botonUnoContraDosCpu = Boton(304, 545, unoContraDosCpuImg, 1)
botonContinuar = Boton(450 ,245,pygame.font.SysFont("arialblack", 40).render("Continuar", True, (255,255,255)),1)
botonOpciones = Boton(450,295,pygame.font.SysFont("arialblack", 40).render("Opciones", True, (255,255,255)),1)
botonComoJugar = Boton(450,345,pygame.font.SysFont("arialblack", 40).render("Como jugar", True, (255,255,255)),1)
botonCreditos = Boton(450,395,pygame.font.SysFont("arialblack", 40).render("Creditos", True, (255,255,255)),1)
botonSalir = Boton(450,445,pygame.font.SysFont("arialblack", 40).render("Salir", True, (255,255,255)),1)
botonSonido = Boton(450,245,pygame.font.SysFont("arialblack", 40).render("Sonido", True, (255,255,255)),1)
botonMusica = Boton(450,295,pygame.font.SysFont("arialblack", 40).render("Musica", True, (255,255,255)),1)
botonDificultad = Boton(450,345,pygame.font.SysFont("arialblack", 40).render("Dificultad", True, (255,255,255)),1)
botonVolver = Boton(450,395,pygame.font.SysFont("arialblack", 40).render("Volver", True, (255,255,255)),1)
botonVolverAzul = Boton(900,600,pygame.font.SysFont("arialblack", 40).render("Volver", True, (255,255,255)),1)


# bucle del juego
ejecucion = True
while ejecucion:
    #Pintar toda la pantalla con el color rgb(52,78,91)
    pantalla.fill((52, 78, 91))
    #si pantalla de pausa es verdadera
    if pantallaDePausa == True:
        #se muestra el fondo celeste y se dibujan los botones
        pantalla.blit(fondoCelesteImg, (0 ,0))
        #se cheaquea que boton se presiona y se abre la ventana correspondiente
        if botonContinuar.dibujar(pantalla):
            print("Continuar")
        if botonOpciones.dibujar(pantalla):
            pantallaDeOpciones = True
            print("Opciones")
        if botonComoJugar.dibujar(pantalla):
            print("Como Jugar") 
        if botonCreditos.dibujar(pantalla):
            print("Creditos") 
        if botonSalir.dibujar(pantalla):
            ejecucion = False
            print("Salir")  
        if pantallaDeOpciones:
            #se muestra el fondo verde con los botones de opciones
            pantalla.blit(fondoVerdeImg,(0, 0))
            if botonSonido.dibujar(pantalla):
                print("Sonido")
            if botonMusica.dibujar(pantalla):
                print("Musica")
            if botonDificultad.dibujar(pantalla):
                print("Dificultad")
            if botonVolver.dibujar(pantalla):
                pantallaDeOpciones = False
    #Si opcionesDeJuego es verdadera           
    elif opcionesDeJuego == True:
        #se selecciona el fondo mediante un condicional
        if pantallaAzul == True:
            pantalla.blit(pantallaAzulImg,(0, 0))
            if botonVolverAzul.dibujar(pantalla):
                pantallaAzul = False
        else:
            #se pone el fondo amarillo
            pantalla.blit(fondoAmarilloImg, (0, 0))
            #Se muestra el titulo
            pantalla.blit(hexajedrezImg, (100, 20))
            #Se dibujan los botones de los modos de juego y al presionarlos cambia la pantalla
            if botonUnoContraUno.dibujar(pantalla):
                pantallaAzul = True
                print("inicia juego 1 contra 1")
            if botonUnoContraDos.dibujar(pantalla):
                pantallaAzul = True
                print("inicia juego 1 contra 2")
            if botonUnoContraCpu.dibujar(pantalla):
                pantallaAzul = True
                print("inicia juego 1 contra CPU")
            if botonUnoContraDosCpu.dibujar(pantalla):
                pantallaAzul = True
                print("inicia juego 1 contra 2 CPU")
    #Si ninguna de las dos variables son verdaderas
    else:
        #se pone el fondo rojo
        pantalla.blit(fondoRojoImg, (0, 0))
        # se dibuja el texto en la pantalla
        dibujaTexto("Presione espacio para comenzar", fuente, COLOR_LETRAS, 304, 500)

    # Escucha eventos
    for evento in pygame.event.get():
        
        # si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
             ejecucion = False
        # si se aprieta una tecla se valida que
        elif evento.type == pygame.KEYDOWN:
            # si la tecla presionada es espacio
            if evento.key == pygame.K_SPACE:
                opcionesDeJuego = True
            #si se presiona la tecla escape
            if evento.key == pygame.K_ESCAPE:
                pantallaDePausa = not pantallaDePausa
                pantallaDeOpciones = False
    #Actualiza la pantalla    
    pygame.display.update()
#cierra el juego
pygame.quit()
# sleep(3)#Prueba para ver la ventana funcionar
