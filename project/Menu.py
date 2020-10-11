"""
menu class for menu screens when selecting what to do

creator: Mark Jacobsen
"""
import pygame
import random
import Obstacle
import Button


class Menu:

    def __init__(self):
        self.buttons = {}
        self.projectiles = []
        self.solid_background_objects = []

    def draw(self, screen):
        """
        draws menu on pygame screen
        :param screen: the pygame screen to draw on
        :returns: None
        """
        for projectile in self.projectiles:
            projectile.draw(screen)
        for solid_object in self.solid_background_objects:
            solid_object.draw(screen)
        for button in self.buttons:
            self.buttons[button].draw(screen)

    def add_button(self, rect, text, color):
        """
        add button to the menu
        :param rect: the rect [x, y, width, height]
        :param text: the text to write in the button
        :param color: color of the button
        :returns: None
        """
        new_button = Button.Button(rect, text, color)
        self.buttons[text] = new_button

    def button_clicked(self, mouse_x, mouse_y):
        """
        checks if any button contains the mouse position
        :param mouse_x: the mouse x coordinate
        :param mouse_y: the mouse y coordinate
        :returns: Button name as str or empty string
        """
        for button in self.buttons:
            if self.buttons[button].clicked_on(mouse_x, mouse_y):
                return button
        return ""

    def add_background_object(self, obj):
        """
        add an object to draw into background
        :param obj: the object to draw
        """
        self.solid_background_objects.append(obj)

