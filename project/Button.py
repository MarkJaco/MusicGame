"""
Button class for making rect buttons with pygame

creator: Mark Jacobsen
"""
import pygame
import Text


class Button:
    def __init__(self, rect, text, color):
        self.rect = rect
        self.text = self.make_text(text)
        self.color = color

    def make_text(self, text):
        """
        make the text object belonging to the button
        :param text: the text message as string
        :returns: None
        """
        text_size = self.rect[2] / 15
        text_point = (0, 0)
        pre_text = Text.Text(text, text_point, text_size)
        rendered_text = pre_text.render()
        text_width = rendered_text.get_width()
        text_height = rendered_text.get_height()
        text_x = int(self.rect[0] + (self.rect[2] / 2) - text_width / 2)
        text_y = int(self.rect[1] + (self.rect[3] / 2) - text_height / 2)
        return Text.Text(text, (text_x, text_y), text_size)

    def draw(self, screen):
        """
        draw button on pygame screen
        :param screen: the screen to draw on
        :returns: None
        """
        pygame.draw.rect(screen, self.color, self.rect, 5)
        self.text.draw(screen)

    def clicked_on(self, mouse_x, mouse_y):
        """
        checks if clicked on
        :param mouse_x: the mouse x coordinate
        :param mouse_y: the mouse y coordinate
        :returns: boolean accordingly
        """
        return pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3]).collidepoint(mouse_x, mouse_y)
