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
        # Origen central del juego.
        ORIGEN_JUEGO = ((ANCHO_JUEGO / 2),(ALTO_JUEGO/2))
        # Pantalla del juego. 
        PANTALLA = pygame.display.set_mode((ALTO_JUEGO,int(ANCHO_JUEGO+(ANCHO_JUEGO*0.36))))

        juegoEjecutandose = True

        # comentario aca
        while juegoEjecutandose:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            PANTALLA.fill((255,255,255))
            pygame.draw.line(PANTALLA,(100,100,100),AREA_ESTADO, AREA_JUEGO)

            PANTALLA.blit(pygame.transform.scale(
                        pygame.image.load(f"img/pantallaAzul.png").convert_alpha(),
                        (700, 700)
                    ),AREA_JUEGO)
            pygame.display.flip()


    print("juego iniciado")