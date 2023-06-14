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
ALTO_PANTALLA = 700

# Se define el tamanio de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), flags=0)

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
pantallaModoDeJuego = False
pantallaDePausa = [False]
juegoEjecutandose = [True]
pantallaDeOpciones = False
pantallaDificultad = False
pantallaCreditos = False

# Se instancia el juego
juego = Juego()

# Opciones:
opciones = [False, "Medio", True, True, False]
"""Bot, dificultad, sonido, musica.""" 

# Variable incrementable de creditos
creditosDesplazamiento: int = 0  

# Imagenes del Menu
unoContraUnoImg = Imagen("img/boton_uno_contra_uno.png")
unoContraDosImg = Imagen("img/boton_uno_contra_dos.png")
unoContraCpuImg = Imagen("img/boton_uno_contra_cpu.png")
unoContraDosCpuImg = Imagen("img/boton_uno_contra_dos_cpu.png")
pausaImg = Imagen("img/boton_Pausa.png")
activadoImg = Imagen("img/caja_activado.png")
desactivadoImg = Imagen("img/caja_desactivado.png")
hexajedrezImg = Imagen("img/HEXajedrez.png")

# Imagen de fondo
fondoRojoImg = Imagen('img/Fondo_Rojo.png')
fondoAmarilloImg = Imagen('img/Fondo_Amarillo.png')
fondoCelesteImg = Imagen('img/Fondo_Celeste.png')
fondoVerdeImg = Imagen('img/Fondo_Verde.jpg')

# Metodos
metodo = Metodos()

# Crear Botones del menu principal
botonUnoContraUno = Boton(0, 485, unoContraUnoImg.obtenerImagen())
botonUnoContraDos = Boton(0, 585, unoContraDosImg.obtenerImagen())
botonUnoContraCpu = Boton(0, 285, unoContraCpuImg.obtenerImagen())
botonUnoContraDosCpu = Boton(0, 385, unoContraDosCpuImg.obtenerImagen())
botonPausa = Boton(1075, 25, pausaImg.obtenerImagen())

# Botones del menu de pausa
botonContinuar = Boton(0, 210, FUENTE.render("Continuar", True, BLANCO))
botonOpciones = Boton(0, 260, FUENTE.render("Opciones", True, BLANCO))
botonComoJugar = Boton(0, 310, FUENTE.render("Como jugar", True, BLANCO))
botonCreditos = Boton(0, 360, FUENTE.render("Creditos", True, BLANCO))
botonMenuPrincipal = Boton(0, 410, FUENTE.render("Menu principal", True, BLANCO))

# Botones del menu de pausa
botonDificultad = Boton(0, 295, FUENTE.render("Dificultad", True, BLANCO))
botonFacil = Boton(280, 295, FUENTE.render("Facil", True, BLANCO))
botonMedio = Boton(0, 295, FUENTE.render("Medio", True, BLANCO))
botonDificil = Boton(820, 295, FUENTE.render("Dificil", True, BLANCO))
botonSalir = Boton(0, 460, FUENTE.render("Salir", True, BLANCO))
botonSonido = Boton(495, 395, FUENTE.render("Sonido", True, BLANCO))
botonMusica = Boton(500, 345, FUENTE.render("Musica", True, BLANCO))
botonPantallaCompleta = Boton(0, 245, FUENTE.render("Maximizar", True, BLANCO))
botonSonidoCheckBox = Boton(660, 395, activadoImg.obtenerImagen())
botonMusicaCheckBox = Boton(660, 345, activadoImg.obtenerImagen())
botonVolver = Boton(0, 445, FUENTE.render("Volver", True, BLANCO))

# Adicion de propiedad de pantalla redimensionable
pantalla = pygame.display.set_mode((825, 525),pygame.RESIZABLE)

# Bucle principal de ejecucion
ejecucion = True
num_canales_originales = 0
# Inicio de musica de menu Principal
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
            anchoPantalla, altoPantalla = pygame.display.get_window_size()
            escala_y = altoPantalla / ALTO_PANTALLA

            # Incremento de desplazamiento de credito 
            creditosDesplazamiento = metodo.creditos(creditosDesplazamiento)
            
            #condicional en el caso de que alcance el borde de la panta
            if creditosDesplazamiento < -(altoPantalla + 300 * escala_y):
        
                # Se abandona la pantalla de creditos
                creditosDesplazamiento = 0
                pantallaCreditos = False

        # PANTALLA DE OPCIONES
        elif pantallaDeOpciones:
            
            # Se muestra el fondo verde con los botones de opciones
            fondoVerdeImg.dibujar(0, 0)

            # Si se presiona el boton de pantalla completa
            if botonPantallaCompleta.dibujar():
                opciones[4] = not opciones[4]

                # Se maximiza la pantalla
                if opciones[4]:
                    botonPantallaCompleta.imagen = FUENTE.render("Minimizar", True, BLANCO)
                    pantalla = pygame.display.set_mode((1360, 738), pygame.RESIZABLE)

                # Se minimiza la pantalla
                else:
                    botonPantallaCompleta.imagen = FUENTE.render("Maximizar", True, BLANCO)
                    pantalla = pygame.display.set_mode((825, 525), pygame.RESIZABLE)

            # se muestran las opciones de musica y sonido asi como sus cajitas de opciones.
            if botonSonido.dibujar() or botonSonidoCheckBox.dibujar():
                opciones[2] = not opciones[2]
                Sonido.volumen = opciones[2]
                botonSonidoCheckBox.imagen = activadoImg.obtenerImagen() if opciones[2] else desactivadoImg.obtenerImagen()
            
            if botonMusica.dibujar() or botonMusicaCheckBox.dibujar():
                opciones[3] = not opciones[3]
                botonMusicaCheckBox.imagen = activadoImg.obtenerImagen() if opciones[3] else desactivadoImg.obtenerImagen()

            # Se muestra las distintas opciones de dificultad.
            if pantallaDificultad:
                desactivadoImg.dibujar(370, 295)
                desactivadoImg.dibujar(650, 295)
                desactivadoImg.dibujar(925, 295)
                if opciones[1] == "Facil":
                    activadoImg.dibujar(370, 295)
                elif opciones[1] == "Medio":
                    activadoImg.dibujar(650, 295)
                else:
                    activadoImg.dibujar(925, 295)
                # Si se elige la dificultad facil:
                if botonFacil.dibujar():
                    opciones[1] = "Facil"
                    pantallaDificultad = False

                # Si se elige la dificultad medio:
                if botonMedio.dibujar():
                    opciones[1] = "Medio"
                    pantallaDificultad = False

                # Si se elige la dificultad dificil:
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

            # Se muestra el fondo celeste y se dibujan los botones
            fondoCelesteImg.dibujar(0, 0)

            # Se chequea que boton se presiona y se abre la ventana correspondiente
            if botonContinuar.dibujar():
                pantallaDePausa[0] = False

            if botonOpciones.dibujar():
                # Abre la pantalla de opciones
                pantallaDeOpciones = True

            if botonComoJugar.dibujar():
                # Se muestran las instrucciones de como jugar.
                metodo.comoJugar()
                pantallaDePausa[0] = False
                
            if botonCreditos.dibujar():
                # Se muestra la Pantalla de Creditos
                creditosDesplazamiento = 600
                metodo.creditos(creditosDesplazamiento)
                pantallaCreditos = True

            if botonMenuPrincipal.dibujar():
                # Se vuelve el programa al menu inicial
                juegoEjecutandose[0] = False
                pantallaModoDeJuego = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("sonido/8-bit-dream-land-142093.mp3")
                pygame.mixer.music.play(-1)
                                
                pantallaDePausa[0] = False
            
            if botonSalir.dibujar():
                # Se abandona el bucle de ejecucion y cierra el programa
                ejecucion = False

    # PANTALLA DE MODOS DE JUEGO
    elif pantallaModoDeJuego == True:

        # Se continua el juego si existe una partida.
        if os.path.exists("registro/Registro de jugadas.txt") and os.path.exists("registro/Estado tablero.txt") :
            archivo = open("registro/Registro de jugadas.txt","r")
            if len(archivo.readlines())>1:
                juegoEjecutandose[0] = True
                juego.iniciar(opciones[1], pantallaDePausa, juegoEjecutandose, "", opciones[0], True, opciones[2], opciones[3])

            archivo.close()
            archivo = None
            
        # Se dibuja el fondo amarillo
        fondoAmarilloImg.dibujar(0, 0)

        # Se muestra el titulo
        hexajedrezImg.dibujar(0, 120)

        # Se dibujan los botones de los modos de juego y al presionarlos cambia la pantalla
        # Boton 1 vs 1
        if botonUnoContraUno.dibujar():
            juegoEjecutandose[0] = True
            juego.iniciar(opciones[1], pantallaDePausa, juegoEjecutandose, "bn",opciones[0], False, opciones[2], opciones[3])
        # Boton 1 vs 2
        if botonUnoContraDos.dibujar():
            juegoEjecutandose[0] = True
            juego.iniciar(opciones[1], pantallaDePausa, juegoEjecutandose, "bnr",opciones[0], False, opciones[2], opciones[3])
        # Boton 1 vs CPU
        if botonUnoContraCpu.dibujar():
            juegoEjecutandose[0] = True
            juego.iniciar(opciones[1], pantallaDePausa, juegoEjecutandose, "bn", True, False, opciones[2], opciones[3])
        # Boton 1 vs 2 CPU
        if botonUnoContraDosCpu.dibujar():
            juegoEjecutandose[0] = True
            juego.iniciar(opciones[1], pantallaDePausa, juegoEjecutandose, "bnr", True, False, opciones[2], opciones[3])
        # Boton de pausa
        if botonPausa.dibujar():
            pantallaDePausa[0] = True

    # PANTALLA DE TITULO
    else:
        # Se dibuja el fondo rojo
        fondoRojoImg.dibujar(0, 0)
        
        # Se dibuja el titulo del juego
        hexajedrezImg.dibujar(0, ALTO_PANTALLA/2)

        # Se dibuja el texto en la pantalla
        if os.path.exists("registro/Registro de jugadas.txt") and len(open("registro/Registro de jugadas.txt","r").readlines())>1 and os.path.exists("registro/Estado tablero.txt"):
            # Si existe una partida, se muestra en pantalla una instruccion para reanudar o comenzar nuevo juego.
            Metodos.dibujarTexto("Hay una partida guardada", 30, (255, 255, 70), 0, 490)
            Metodos.dibujarTexto("Presione ESPACIO para continuar", 20, BLANCO, 0, 540)
            Metodos.dibujarTexto("o N para comenzar nuevo juego", 20, BLANCO, 0, 580)
        else:
            # Si no hay partida guardada aparece el mensaje original .
            Metodos.dibujarTexto("Presione ESPACIO para comenzar", 30, BLANCO, 0, 500)
            Metodos.dibujarTexto("o ESCAPE para mas opciones", 20, BLANCO, 0, 550)
    
    # Escucha eventos
    for evento in pygame.event.get():

        # Si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
            ejecucion = False

        # Actualizar la ventana al redimensionar
        elif evento.type == pygame.KEYDOWN:

            # Si la tecla presionada es espacio
            if evento.key == pygame.K_SPACE:
                pantallaModoDeJuego = True

            # Si se presiona la tecla escape
            if evento.key == pygame.K_ESCAPE:
                juegoEjecutandose[0] = not juegoEjecutandose[0]
                pantallaDePausa[0] = not pantallaDePausa[0]
                pantallaDeOpciones = False
                pantallaDificultad = False
                pantallaCreditos = False
            
            # Si se presiona la letra n
            if evento.key == pygame.K_n:
                #activa 
                pantallaModoDeJuego = True
                if os.path.exists("registro/Registro de jugadas.txt"):
                    # Si existe el registro, se borra.
                    os.remove("registro/Registro de jugadas.txt")

                if os.path.exists("registro/Estado tablero.txt"):
                    # Si existe el estado, se borra.
                    os.remove("registro/Estado tablero.txt")

    # Actualiza la pantalla
    pygame.display.update()

# Cierra el programa
pygame.quit()
