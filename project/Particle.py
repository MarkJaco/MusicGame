"""
particle animations for e.g destroy animations of blocks

creator: Mark Jacobsen
"""
import pygame
from helper import colors


class Particle:
    def __init__(self, pos, color):
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.color = color
        self.size = 0
        self.growth_rate = 5
        self.width = 3
        self.max_size = 100

    def move(self):
        """
        changes in particle effects take place here
        like size changes
        :returns: None
        """
        self.size += self.growth_rate

    def draw(self, screen):
        """
        draws particle on pygame screen
        :param screen: the pygame screen to draw on
        :returns: None
        """
        if self.size <= self.max_size:
            pygame.draw.circle(screen, self.color, [self.x, self.y], self.size, self.width)
