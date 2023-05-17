import pygame

class Juego:
    
    def __init__(self,x):
        # Dimensión del juego.
        self.AREA_JUEGO = (x*0.63, x*0.63)  
        # Dimensión adicional necesaria para la GUI.
        self.AREA_ESTADO = (x*0.36, 0)  

    def iniciar(self):
        pygame.init()
        # Dimensión del juego.
        AREA_JUEGO= self.AREA_JUEGO 
        # Dimensión adicional necesaria para la GUI.
        AREA_ESTADO= self.AREA_ESTADO  
        # Ancho y alto del juego.
        ANCHO_JUEGO, ALTO_JUEGO = AREA_JUEGO
        ANCHO_ESTADO, ALTO_ESTADO = AREA_ESTADO
        # Origen central del juego.
        ORIGEN_JUEGO = ((ANCHO_JUEGO / 2),(ALTO_JUEGO/2))
        # Pantalla del juego. 
        
        PANTALLA = pygame.display.set_mode((ANCHO_JUEGO+ANCHO_ESTADO,ALTO_JUEGO))
        
        juegoEjecutandose = True
        
        # Bucle del juego
        while juegoEjecutandose:
            for evento in pygame.event.get():
                #si se pulsa la cruz para salir, se cierra la ventana y el programa
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # se pone la pantalla de color blanco
            PANTALLA.fill((255,255,255))
            
            # se muestra la del juego con la imagen "Fondo_Juego.jpg"
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Estado.jpg").convert_alpha(),(1100, 700)),(0,0))
            PANTALLA.blit(pygame.transform.scale(pygame.image.load(f"img/Fondo_Juego.png").convert_alpha(),(700, 700)),(-5,-2))
            
            # se dibuja la linea que va a separar el tablero con la GUI de informacion
            pygame.draw.line(PANTALLA,(62,48,92),(ANCHO_JUEGO, 0), (ANCHO_JUEGO, ALTO_JUEGO),13)

            #actualiza la pantalla
            pygame.display.flip()


    print("juego iniciado")