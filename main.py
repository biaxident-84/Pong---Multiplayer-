import pygame
import sys
from constantes import *
from utilidades import colision_pelota_paleta, mostrar_puntaje
from paleta import Paleta
from pelota import Pelota


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/retro_back.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# Efectos de sonido
sonido_paleta = pygame.mixer.Sound("assets/sounds/paleta.mp3")
sonido_paleta.set_volume(0.5)
sonido_pared = pygame.mixer.Sound("assets/sounds/rebote.wav")
sonido_pared.set_volume(0.5)
sonido_gol = pygame.mixer.Sound("assets/sounds/goal.wav")
sonido_gol.set_volume(0.5)
sonido_game_over = pygame.mixer.Sound("assets/sounds/win.wav")
sonido_game_over.set_volume(0.4)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong - Multiplayer")
# Cargo el fondo y escalo la imagen
fondo_original = pygame.image.load("assets/images/fondo.jpg")
fondo = pygame.transform.scale(fondo_original, (ANCHO, ALTO))

clock = pygame.time.Clock()

# Paleta del jugador N°1 izquierda
paleta_izq = Paleta(
    x = 30, # 30 pixeles desde el borde izquierdo
    y = ALTO // 2 - PALETA_ALTO // 2, # Centrada verticalmente
    ancho = PALETA_ANCHO,
    alto = PALETA_ALTO,
    velocidad = PALETA_VEL,
    color = BLANCO
)

paleta_der = Paleta(
    x = ANCHO - 30 - PALETA_ANCHO,  # 30 pixeles desde el borde derecho
    y = ALTO // 2 - PALETA_ALTO // 2, # Centrada verticalmente
    ancho = PALETA_ANCHO,
    alto = PALETA_ALTO,
    velocidad = PALETA_VEL,
    color =  BLANCO
)

# Pelota centrada en la pantalla
pelota = Pelota(
    x = ANCHO //2,
    y = ALTO //2,
    radio = PELOTA_RADIO,
    velocidad_x = PELOTA_VEL_X,
    velocidad_y = PELOTA_VEL_Y,
    color = BLANCO
)

# Puntaje inicial 
puntaje_jug1 = 0
puntaje_jug2 = 0

# Contador de rebotes
contador_rebotes = 0

#Estado del juego
game_over = False
ganador = None

def manejar_rebote_paletas(pelota, paleta, lado):

    """Maneja colision de peloota con paleta

    Args:
        pelota (_type_): Objeto pelota
        paleta (_type_): Objeto paleta con la que colisiona la pelota
        lado (_type_): "izquierda" o "derecha"
    """
    global contador_rebotes

    #reposiciona la pelota según el lado
    if lado == "izquierda":
        pelota.x = paleta.x + paleta.ancho + pelota.radio
    else:
        pelota.x = paleta.x - pelota.radio

    pelota.rebotar_horizontal()
    sonido_paleta.play()

    contador_rebotes += 1

    # Aumento de velocidad
    if contador_rebotes % 3 == 0:
        pelota.velocidad_x *= 1.1
        pelota.velocidad_y *= 1.1

    # Control de la velocidad x (evita un aumento excesivo)
    if pelota.velocidad_x > MAX_VELOCIDAD:
        pelota.velocidad_x = MAX_VELOCIDAD
    elif pelota.velocidad_x < -MAX_VELOCIDAD:
        pelota.velocidad_x = -MAX_VELOCIDAD
    # Velocidad y       
    if pelota.velocidad_y > MAX_VELOCIDAD:
        pelota.velocidad_y = MAX_VELOCIDAD
    elif pelota.velocidad_y < -MAX_VELOCIDAD:
        pelota.velocidad_y = -MAX_VELOCIDAD
   

#========== GAME LOOP =======(lógica del juego)

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if not game_over:
        # === CONTROLES ===
        #Jugador N° 1 (teclas W/S)
        if pygame.key.get_pressed()[pygame.K_w]:
            paleta_izq.mover_arriba(0)
        if pygame.key.get_pressed()[pygame.K_s]:
            paleta_izq.mover_abajo(ALTO)

        #Jugador N° 2 ( teclas arriba/abajo)
        if pygame.key.get_pressed()[pygame.K_UP]:
            paleta_der.mover_arriba(0)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            paleta_der.mover_abajo(ALTO)

        # === ACTUALIZAR ===
        pelota.mover()

        # === COLISIONES ===
        """ Rebote con el borde superior de la cancha"""
        if pelota.y - pelota.radio <= 0:
            pelota.y = pelota.radio
            pelota.rebotar_vertical()
            sonido_pared.play()

        """ Rebote con el borde inferior de la cancha"""
        if pelota.y + pelota.radio >= ALTO:
            pelota.y = ALTO - pelota.radio
            pelota.rebotar_vertical()
            sonido_pared.play()

        if colision_pelota_paleta(pelota, paleta_izq):
            manejar_rebote_paletas(pelota, paleta_izq, "izquierda")

        if colision_pelota_paleta(pelota, paleta_der):
            manejar_rebote_paletas(pelota, paleta_der, "derecha")

        # === GOLES ===

        #Gol de jugador N°2( la pelota sale por la izquierda)
        if pelota.x - pelota.radio <= 0:
            sonido_gol.play()
            puntaje_jug2 += 1
            pelota.reiniciar(ANCHO, ALTO)
            contador_rebotes = 0

            if puntaje_jug2 >= PUNTOS_GANADOR:
                game_over = True
                ganador = 2
                sonido_game_over.play()
            
        #Gol de jugador N°1 ( la pelota sale por la derecha)
        if pelota.x + pelota.radio >= ANCHO:
            sonido_gol.play()
            puntaje_jug1 += 1
            pelota.reiniciar(ANCHO, ALTO)
            contador_rebotes = 0

            if puntaje_jug1 >= PUNTOS_GANADOR:
                game_over = True
                ganador = 1
                sonido_game_over.play()



    #Dibujar 
    pantalla.blit(fondo, (0, 0))
    

    if not game_over:
        #Linea centrar de decoracion (red)
        pygame.draw.line(pantalla, GRIS, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

        #Mostrar el puntaje 
        mostrar_puntaje(pantalla, puntaje_jug1, puntaje_jug2)

        #Dibujar los objetos del juego
        paleta_izq.dibujar(pantalla)
        paleta_der.dibujar(pantalla)
        pelota.dibujar(pantalla)
    else:
        fuente = pygame.font.Font(None, 95)
        texto = fuente.render("GANADOR JUGADOR " + str(ganador)+"!", True, ROJO)
        pos_x = ANCHO // 2 - texto.get_width() // 2
        pos_y = ALTO //2 - texto.get_height() // 2
        pantalla.blit(texto, (pos_x, pos_y))

        fuente_pequeña = pygame.font.Font(None, 40)
        texto_salir = fuente_pequeña.render("Presione ESC para salir", True, GRIS)
        pos_x_salir = ANCHO // 2 - texto_salir.get_width() // 2
        pos_y_salir = ALTO // 2 + 50
        pantalla.blit(texto_salir, (pos_x_salir, pos_y_salir))

    #Mostrando los dibujos
    pygame.display.flip()

    #Control del FPS
    clock.tick(FPS)





#toque espacio si quiere seguir jugando, ingreso de nombre del jugador al inicio 
