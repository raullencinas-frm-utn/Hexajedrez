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
pantallaDePausa = False
pantallaDeOpciones = False
pantallaAzul = False

# Funciones


def dibujaTexto(texto, tamanio, colorTexto, x, y):
    """ Genenera un texto en pantalla con la FUENTE y color de texto elegidos en la 
    posicion "x" e "y" de la pantalla con el texto elegido. """
    img = pygame.font.Font(
        "fnt/8-Bit.TTF", tamanio).render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))


# Imagenes del Menu
unoContraUnoImg = Imagen("img/boton_uno_contra_uno.png")
unoContraDosImg = Imagen("img/boton_uno_contra_dos.png")
unoContraCpuImg = Imagen("img/boton_uno_contra_cpu.png")
unoContraDosCpuImg = Imagen("img/boton_uno_contra_dos_cpu.png")

# Titulo menu
hexajedrezImg = Imagen("img/HEXajedrez.png")


# Imagen de fondo
fondoRojoImg = Imagen('img/Fondo_Rojo.png')
fondoAmarilloImg = Imagen('img/Fondo_Amarillo.png')
fondoCelesteImg = Imagen('img/Fondo_Celeste.png')
fondoVerdeImg = Imagen('img/Fondo_Verde.jpg')
pantallaAzulImg = Imagen('img/pantallaAzul.png')

# Crear Botones
botonUnoContraUno = Boton(0, 245, unoContraUnoImg.obtenerImagen(), 1)
botonUnoContraDos = Boton(0, 345, unoContraDosImg.obtenerImagen(), 1)
botonUnoContraCpu = Boton(0, 445, unoContraCpuImg.obtenerImagen(), 1)
botonUnoContraDosCpu = Boton(0, 545, unoContraDosCpuImg.obtenerImagen(), 1)
botonContinuar = Boton(0, 245, FUENTE.render("Continuar", True, BLANCO), 1)
botonOpciones = Boton(0, 295, FUENTE.render("Opciones", True, BLANCO), 1)
botonComoJugar = Boton(0, 345, FUENTE.render("Como jugar", True, BLANCO), 1)
botonCreditos = Boton(0, 395, FUENTE.render("Creditos", True, BLANCO), 1)
botonSalir = Boton(0, 445, FUENTE.render("Salir", True, BLANCO), 1)
botonSonido = Boton(0, 245, FUENTE.render("Sonido", True, BLANCO), 1)
botonMusica = Boton(0, 295, FUENTE.render("Musica", True, BLANCO), 1)
botonDificultad = Boton(0, 345, FUENTE.render("Dificultad", True, BLANCO), 1)
botonVolver = Boton(0, 395, FUENTE.render("Volver", True, BLANCO), 1)
botonVolverAzul = Boton(850, 600, FUENTE.render("Volver", True, BLANCO), 1)


# Bucle de ejecucion
ejecucion = True
while ejecucion:
    # Pintar la pantalla de color blanco
    pantalla.fill(BLANCO)

    # PANTALLA DE PAUSA
    if pantallaDePausa == True:
        # se muestra el fondo celeste y se dibujan los botones
        pantalla.blit(fondoCelesteImg.redimensionar(
            ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
        # se chequea que boton se presiona y se abre la ventana correspondiente
        if botonContinuar.dibujar("Centrado"):
            print("Continuar")
        if botonOpciones.dibujar("Centrado"):
            # Abre la pantalla de opciones
            pantallaDeOpciones = True
            print("Opciones")
        if botonComoJugar.dibujar("Centrado"):
            print("Como Jugar")
        if botonCreditos.dibujar("Centrado"):
            print("Creditos")
        if botonSalir.dibujar("Centrado"):
            # Se abandona el bucle de ejecucion y cierra el programa
            ejecucion = False
            print("Salir")
        # PANTALLA DE OPCIONES
        if pantallaDeOpciones:
            # se muestra el fondo verde con los botones de opciones
            pantalla.blit(fondoVerdeImg.redimensionar(
                ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
            if botonSonido.dibujar("Centrado"):
                print("Sonido")
            if botonMusica.dibujar("Centrado"):
                print("Musica")
            if botonDificultad.dibujar("Centrado"):
                print("Dificultad")
            if botonVolver.dibujar("Centrado"):
                # Se abandona la pantalla de opciones
                pantallaDeOpciones = False
    # PANTALLA DE MODOS DE JUEGO
    elif opcionesDeJuego == True:
        # Se selecciona el fondo mediante un condicional
        if pantallaAzul == True:
            pantalla.blit(pantallaAzulImg.redimensionar(
                ANCHO_PANTALLA, ALTO_PANTALLA), (0, 0))
            if botonVolverAzul.dibujar(""):
                pantallaAzul = False
        else:
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
        dibujaTexto("Presione ESPACIO para comenzar", 30, BLANCO, 130, 500)
        dibujaTexto("o ESCAPE para mas opciones", 20, BLANCO, 295, 550)

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
                pantallaDePausa = not pantallaDePausa
                pantallaDeOpciones = False

    # Actualiza la pantalla
    pygame.display.update()
# Cierra el programa
pygame.quit()
# sleep(3) # Prueba para ver la ventana funcionar
