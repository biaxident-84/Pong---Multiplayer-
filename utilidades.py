import pygame
from constantes import ANCHO, BLANCO


#=== Detectar colision =====
def colision_pelota_paleta(pelota, paleta):
    """ Detecta si la pelota colisiona con una paleta

    Args:
        pelota (_type_): Objeto pelota con atributos x, y, radio
        paleta (_type_): Objeto palete con atributos x, y, ancho y alto

    Returns:
        True si hay colision y False sino
    """
    pelota_rect = pygame.Rect(
        pelota.x - pelota.radio,
        pelota.y - pelota.radio,
        pelota.radio * 2,
        pelota.radio * 2
    )
    paleta_rect = pygame.Rect(
        paleta.x,
        paleta.y,
        paleta.ancho,
        paleta.alto
    )
    return pelota_rect.colliderect(paleta_rect)

def mostrar_puntaje(pantalla, puntaje_jug1, puntaje_jug2, tamaño_fuente=85):

    fuente = pygame.font.Font(None, tamaño_fuente)

    texto_jug1 = fuente.render(str(puntaje_jug1), True, BLANCO)
    texto_jug2 = fuente.render(str(puntaje_jug2), True, BLANCO)

    # Calculo de las posiciones centradas
    pos_x_jug1 = ANCHO // 4 - texto_jug1.get_width() //2
    pos_y_jug2 = 3 * ANCHO // 4 - texto_jug2.get_width() // 2

    # Dibuja en pantalla
    pantalla.blit(texto_jug1, (pos_x_jug1, 20))
    pantalla.blit(texto_jug2, (pos_y_jug2, 20))

