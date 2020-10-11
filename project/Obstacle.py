"""
obstacle module contains obstacle class
if an obstacle hits the player it is game over

creator: Mark Jacobsen
"""
import random
import pygame
from helper import colors
import Particle


class Obstacle:
    def __init__(self, location, size):
        self.x = location[0]
        self.y = location[1]
        self.size = size
        self.color = colors["black"]
        self.rect = [location[0], location[1], size, size]

    def __repr__(self):
        return f"Obstacle at {self.x, self.y}, with size of {self.size}"

    def invert_color(self):
        """
        invert the obstacles color
        :returns: None
        """
        if self.color == colors["white"]:
            self.color = colors["black"]
        elif self.color == colors["black"]:
            self.color = colors["white"]

    def set_rect(self):
        """
        sets the obstacle rect
        """
        self.rect = [self.x, self.y, self.size, self.size]

    def draw(self, screen):
        """
        draw rect on pygame screen
        :param screen: the pygame screen to draw onto
        :returns: None
        """
        pygame.draw.rect(screen, self.color, self.rect)

    def intersects_player(self, player):
        """
        checks for obstacle intersection with player
        :param player: player object
        :returns: boolean accordingly
        """
        right = self.x + self.size
        if (self.x <= player.x - player.size <= right) or (self.x <= player.x + player.size <= right):
            bottom = self.y + self.size
            if (self.y <= player.y - player.size <= bottom) or (self.y <= player.y + player.size <= bottom):
                return True
        return False

    def move(self, movement, player):
        """
        move the obstacle
        :param movement: the movement speed and direction as int
        :param player: the player object
        :returns: None
        """
        self.x += movement
        self.set_rect()


class Projectile(Obstacle):

    def __init__(self, location, size):
        super().__init__(location, size)
        self.side = "right"
        self.steps = 0
        self.color_change_amount = 10
        self.destroyed = False

    def change_color_random(self):
        """
        changes projectile color to random color
        :returns: None
        """
        self.color = colors[random.choice(["red", "green", "yellow", "orange", "blue"])]

    def draw(self, screen):
        """
        draw rect on pygame screen
        :param screen: the pygame screen to draw onto
        :returns: None
        """
        if self.destroyed:
            return
        super().draw(screen)

    def intersects_player(self, player):
        """
        checks for obstacle intersection with player
        :param player: player object
        :returns: boolean accordingly
        """
        if self.destroyed:
            return False
        return super().intersects_player(player)

    def move(self, movement, player):
        """
        move the projectile
        and change color
        :param movement: the direction and speed of movement as num
        :param player: the player object
        :returns: None
        """
        if self.destroyed:
            return
        # keep y as player y
        self.y = player.y
        # move along x-axis
        if self.side == "right":
            self.x += movement
        else:
            self.x -= movement
        self.set_rect()
        if self.steps % self.color_change_amount == 0:
            self.change_color_random()
        self.steps += 1

    def destroy(self):
        """
        self-destruct
        :returns: death particle animation object
        """
        self.destroyed = True
        return Particle.Particle([self.x, self.y], self.color)
