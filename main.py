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

#==== Efectos de sonido ====
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

# Posicion Paleta del jugador N°1 izquierda
paleta_izq = Paleta(
    x = 30, # 30 pixeles desde el borde izquierdo
    y = ALTO // 2 - PALETA_ALTO // 2, # Centrada verticalmente
    ancho = PALETA_ANCHO,
    alto = PALETA_ALTO,
    velocidad = PALETA_VEL,
    color = BLANCO
)
# Posición Paleta del jugador N°2 derecha
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
nombre_jug1 = ""
nombre_jug2 = ""
estado_act = ESTADO_INICIO
capt_jugador1 = True

#  **** Funciones Auxiliares ****
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

def reiniciar_juego():
    """ Reinicia al juego luego de un Game Over.
    resetea:
    - Posición de la pelota llamando a la funcion reiniciar
    - Puntajes de ambos jugadores
    - Contador de rebotes ( velocidad de pelota)
    - Estado del juego y Ganador
    - Reseteo velocidades de pelota manualmente
    """
    global puntaje_jug1, puntaje_jug2,contador_rebotes, estado_act, ganador

    pelota.reiniciar(ANCHO, ALTO)

    pelota.velocidad_x = PELOTA_VEL_X
    pelota.velocidad_y = PELOTA_VEL_Y
    puntaje_jug1 = 0
    puntaje_jug2 = 0
    contador_rebotes = 0
    estado_act = ESTADO_JUEGO
    ganador = None

#========== GAME LOOP =======(lógica del juego)

while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado_act == ESTADO_GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        if estado_act == ESTADO_GAME_OVER:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_juego()

        if estado_act == ESTADO_INICIO:
            if evento.type == pygame.KEYDOWN:

                if capt_jugador1:
                    if evento.key == pygame.K_RETURN:
                        capt_jugador1 = False

                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_jug1 = nombre_jug1[: -1]

                    elif len(nombre_jug1) < 10 and evento.unicode.isprintable():
                        nombre_jug1 += evento.unicode  # agrega letra
                
                else:
                    if evento.key == pygame.K_RETURN:
                        if not nombre_jug1:
                            nombre_jug1 = "jugador 1"
                        if not nombre_jug2:
                            nombre_jug2 = "jugador 2"
                        estado_act = ESTADO_JUEGO
            
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_jug2 = nombre_jug2[:-1]
            
                    elif len(nombre_jug2) < 10 and evento.unicode.isprintable():
                        nombre_jug2 += evento.unicode

    if estado_act == ESTADO_INICIO:
        pass

    if estado_act == ESTADO_JUEGO:

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
                estado_act = ESTADO_GAME_OVER
                ganador = 2
                sonido_game_over.play()
            
        #Gol de jugador N°1 ( la pelota sale por la derecha)
        if pelota.x + pelota.radio >= ANCHO:
            sonido_gol.play()
            puntaje_jug1 += 1
            pelota.reiniciar(ANCHO, ALTO)
            contador_rebotes = 0

            if puntaje_jug1 >= PUNTOS_GANADOR:
                estado_act = ESTADO_GAME_OVER
                ganador = 1
                sonido_game_over.play()
    
    if estado_act == ESTADO_GAME_OVER:
        pass


    #Dibujar 
    pantalla.blit(fondo, (0, 0))

    if estado_act == ESTADO_INICIO:
         # Título PONG
        fuente_titulo = pygame.font.Font(None, 100)
        texto_titulo = fuente_titulo.render("PONG", True, BLANCO)
        pos_titulo_x = ANCHO // 2 - texto_titulo.get_width() // 2
        pantalla.blit(texto_titulo, (pos_titulo_x, 100))
        
        # Capturando Jugador 1
        if capt_jugador1:
            fuente = pygame.font.Font(None, 50)
            texto = fuente.render(f"Jugador 1: {nombre_jug1}_", True, BLANCO)
            pos_x = ANCHO // 2 - texto.get_width() // 2
            pantalla.blit(texto, (pos_x, 300))
            
            fuente_info = pygame.font.Font(None, 30)
            texto_info = fuente_info.render("Presiona ENTER para continuar", True, GRIS)
            pos_info_x = ANCHO // 2 - texto_info.get_width() // 2
            pantalla.blit(texto_info, (pos_info_x, 400))
        
        # Capturando Jugador 2
        else:
            fuente = pygame.font.Font(None, 50)
            
            # Jugador 1 confirmado (en verde)
            texto1 = fuente.render(f"Jugador 1: {nombre_jug1}", True, ROJO)
            pos_x1 = ANCHO // 2 - texto1.get_width() // 2
            pantalla.blit(texto1, (pos_x1, 250))
            
            # Jugador 2 escribiendo (en blanco)
            texto2 = fuente.render(f"Jugador 2: {nombre_jug2}_", True, BLANCO)
            pos_x2 = ANCHO // 2 - texto2.get_width() // 2
            pantalla.blit(texto2, (pos_x2, 350))
            
            fuente_info = pygame.font.Font(None, 30)
            texto_info = fuente_info.render("Presiona ENTER para comenzar", True, GRIS)
            pos_info_x = ANCHO // 2 - texto_info.get_width() // 2
            pantalla.blit(texto_info, (pos_info_x, 450))
        

    if estado_act == ESTADO_JUEGO:
        #Linea centrar de decoracion (red)
        pygame.draw.line(pantalla, GRIS, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)

        #Mostrar el puntaje 
        mostrar_puntaje(pantalla, puntaje_jug1, puntaje_jug2)

        #Dibujar los objetos del juego
        paleta_izq.dibujar(pantalla)
        paleta_der.dibujar(pantalla)
        pelota.dibujar(pantalla)

    elif estado_act == ESTADO_GAME_OVER:

        fuente = pygame.font.Font(None, 95)
        texto = fuente.render("GANADOR JUGADOR " + str(ganador)+"!", True, ROJO)
        pos_x = ANCHO // 2 - texto.get_width() // 2
        pos_y = ALTO //2 - texto.get_height() // 2
        pantalla.blit(texto, (pos_x, pos_y))

        fuente_salir = pygame.font.Font(None, 40)
        texto_salir = fuente_salir.render("Presione ESC para salir", True, GRIS)
        pos_x_salir = ANCHO // 2 - texto_salir.get_width() // 2
        pos_y_salir = ALTO // 2 + 50
        pantalla.blit(texto_salir, (pos_x_salir, pos_y_salir))

        fuente_continuar = pygame.font.Font(None, 40)
        texto_continuar = fuente_continuar.render("Presione Espacio para continuar", True, GRIS)
        pos_x_continuar = ANCHO // 2 - texto_continuar.get_width() // 2
        pos_y_continuar = ALTO // 2 + 90
        pantalla.blit(texto_continuar, (pos_x_continuar, pos_y_continuar))


    #Mostrando los dibujos
    pygame.display.flip()

    #Control del FPS
    clock.tick(FPS)






