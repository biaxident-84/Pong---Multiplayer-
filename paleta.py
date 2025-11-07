import pygame


class Paleta:
    def __init__(self, x, y, ancho, alto, velocidad, color):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.color = color
        
    def mover_arriba(self, limite_superior):
        self.y -= self.velocidad
        if self.y < limite_superior:
            self.y = limite_superior
        

    def mover_abajo(self, limite_inferior):
        self.y += self.velocidad
        if self.y + self.alto > limite_inferior:
            self.y = limite_inferior - self.alto
        

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))
        