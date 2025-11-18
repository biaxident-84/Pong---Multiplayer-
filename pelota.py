import pygame

class Pelota:
    def __init__(self, x, y, radio, velocidad_x, velocidad_y, color):
        self.x = x
        self.y = y
        self.radio = radio
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.color = color
        
        
    def mover(self):
        """ Mueve la pelota segun sus velocidades"""
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
    def rebotar_vertical(self):
        """ Ya sea que rebote arriba o abajo se invierte la velocidad y"""
        self.velocidad_y *= - 1

    def rebotar_horizontal(self):
        """ Al rebotar en las paletas invierte la velocidad x """
        self.velocidad_x *= - 1

    def reiniciar(self, ancho_pantalla, alto_pantalla):
        """ Reinicia la pelota despues de un punto"""
        self.x = ancho_pantalla // 2
        self.y = alto_pantalla // 2
        #Invierte la velocidad después de un tanto.
        self.velocidad_x *= - 1

    def dibujar(self, pantalla):
        """Dibuja la pelota como un circulo"""
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)
        
