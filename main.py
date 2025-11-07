import pygame
import sys
from paleta import Paleta
from pelota import Pelota

# CONSTANTES del juego
ANCHO = 800
ALTO = 600

#Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)

FPS = 60

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong - Multiplayer")
clock = pygame.time.Clock()

# Configuracion de las paletas
PALETA_ANCHO = 15
PALETA_ALTO = 100
PALETA_VEL = 7

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
    ancho = PALETA_ANCHO,
    velocidad = PALETA_VEL,
    color =  BLANCO
)

# Configuracion de la pelota
PELOTA_RADIO = 10
PELOTA_VEL_Y = 5
PELOTA_VEL_X = 5

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

#===== GAME LOOP ===================

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
    if pygame.key.get_pressed()[pygame.KEYUP]:
        paleta_der.mover_arriba(0)
    if pygame.key.get_pressed()[pygame.KEYDOWN]:
        paleta_der.mover_abajo(ALTO)

# ACTUALIZAR 
pelota.mover()

#COLISIONES en sgte Fase

#Dibujar 
pantalla.fill(NEGRO) # limpia pantalla

#Linea centrar de decoracion (red)
pygame.draw.line(pantalla, Gris, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

#Dibujar los objetos del juego
paleta_izq.dibujar(pantalla)
paleta_der.dibujar(pantalla)
pelota.dibujar(pantalla)

#Mostrando los dibujos
pygame.display.flip()

#Control del FPS
clock.tick(FPS)



