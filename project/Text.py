"""
The Text class makes it easier to handle drawing text in pygame

creator: Mark Jacobsen
"""
import pygame
import pygame.freetype
from helper import colors


class Text:
    def __init__(self, display_text, point, size):
        self.display_text = display_text
        self.point = point
        self.font = pygame.freetype.Font("fonts/arial.ttf", size)
        self.color = colors["black"]

    def render(self):
        """
        render the given text with pygame
        :returns: the rendered text
        """
        text_surface, rect = self.font.render(self.display_text, self.color)
        return text_surface

    def draw(self, screen):
        """
        display the text on pygame surface
        :param screen: the pygame screen
        :returns: None
        """
        rendered_text = self.render()
        screen.blit(rendered_text, self.point)

