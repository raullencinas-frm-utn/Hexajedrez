import pygame
from time import sleep

pygame.init()

#Se crea la ventana principal del programa
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 700

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
 

#Titulo de la pantall
pygame.display.set_caption("HEXajedrez")

icono = pygame.image.load("img/hex_icon.png")
pygame.display.set_icon(icono)

#se define la tipografia
fuente = pygame.font.SysFont("arialblack", 40)
#se define el color de las letras
COLOR_LETRAS = (255, 255, 255)

#Imagen de fondo
fondo_rojo_img = pygame.transform.scale(pygame.image.load('img/Back_Red.png').convert_alpha(),(ANCHO_PANTALLA, ALTO_PANTALLA)) 

#Funciones
def dibujaTexto(texto, fuente, colorTexto, x, y):
    img = fuente.render(texto, True, colorTexto)
    pantalla.blit(img, (x, y))



#bucle del juego
ejecucion = True
while ejecucion:
    pantalla.fill((52,78,91))
    
    pantalla.blit(fondo_rojo_img, (0,0))
    #se dibuja el texto en la pantalla 
    dibujaTexto("Presione espacio para comenzar", fuente, COLOR_LETRAS, 200, 500)

    #Escucha eventos
    for evento in pygame.event.get():
        #si se aprieta una tecla se valida que 
        if evento.type == pygame.KEYDOWN:  
            #si la tecla presionada es espacio
            if evento.key == pygame.K_SPACE:
                print("MENU DE OPCIONES")
        #si se presiona el boton de cierre se termina el bucle
        if evento.type == pygame.QUIT:
            ejecucion = False
    pygame.display.update()
pygame.quit()
#sleep(3)#Prueba para ver la ventana funcionar
