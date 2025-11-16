import pygame
import sys
from constantes import *
from utilidades import colision_pelota_paleta, mostrar_puntaje
from paleta import Paleta
from pelota import Pelota


pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong - Multiplayer")
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


#========== GAME LOOP =======(lógica del juego)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    # ACTUALIZAR 
    pelota.mover()

    # COLISIONES 
    """ Rebote con el borde superior de la cancha"""
    if pelota.y - pelota.radio <= 0:
        pelota.y = pelota.radio
        pelota.rebotar_vertical()

    """ Rebote con el borde inferior de la cancha"""
    if pelota.y - pelota.radio >= ALTO:
        pelota.y = ALTO - pelota.radio
        pelota.rebotar_vertical()

    """ Rebore con paleta izquierda """
    if colision_pelota_paleta(pelota, paleta_izq):
        pelota.x = paleta_izq.x + paleta_izq.ancho + pelota.radio
        pelota.rebotar_horizontal()
        contador_rebotes += 1

        # Aumento de velocidad
        if contador_rebotes % 3 == 0:
            pelota.velocidad_x *= 1.1
            pelota.velocidad_y *= 1.1

        # Control de la velocidad (evita un aumento excesivo)
        if pelota.velocidad_x > MAX_VELOCIDAD:
            pelota.velocidad_x = MAX_VELOCIDAD
        elif pelota.velocidad_x < -MAX_VELOCIDAD:
            pelota.velocidad_x = -MAX_VELOCIDAD

    """ Rebote con la paleta derecha"""
    if colision_pelota_paleta(pelota, paleta_der):
        pelota.x = paleta_der.x - pelota.radio
        pelota.rebotar_horizontal()
        contador_rebotes += 1

        if contador_rebotes % 3 == 0:
            pelota.velocidad_x *= 1.1
            pelota.velocidad_y *= 1.1
        
        if pelota.velocidad_x > MAX_VELOCIDAD:
            pelota.velocidad_x = MAX_VELOCIDAD
        elif pelota.velocidad_x < -MAX_VELOCIDAD:
            pelota.velocidad_x = -MAX_VELOCIDAD

    # --- GOLES ---

    #Gol de jugador N°2( la pelota sale por la izquierda)
    if pelota.x - pelota.radio <= 0:
        puntaje_jug2 += 1
        pelota.reiniciar(ANCHO, ALTO)
        contador_rebotes = 0
        
    #Gol de jugador N°1 ( la pelota sale por la derecha)
    if pelota.x + pelota.radio >= ANCHO:
        puntaje_jug1 += 1
        pelota.reiniciar(ANCHO, ALTO)
        contador_rebotes = 0
        
        
    #Dibujar 
    pantalla.fill(NEGRO) # limpia pantalla

    #Linea centrar de decoracion (red)
    pygame.draw.line(pantalla, GRIS, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

    #Mostrar el puntaje 
    mostrar_puntaje(pantalla, puntaje_jug1, puntaje_jug2)


    #Dibujar los objetos del juego
    paleta_izq.dibujar(pantalla)
    paleta_der.dibujar(pantalla)
    pelota.dibujar(pantalla)

    #Mostrando los dibujos
    pygame.display.flip()

    #Control del FPS
    clock.tick(FPS)


# funciones a desarrollar
# Tablero de punto, aumento de la velocidad de la aplicacion, score y game over 



