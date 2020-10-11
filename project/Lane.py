"""
module contains lane class
the lane class is one possible lane for the player to walk on

creator: Mark Jacobsen
"""
from helper import colors
import pygame
import Obstacle


class Lane:

    def __init__(self, start_point, width, height):
        self.top_left = start_point
        self.bottom_left = (start_point[0], start_point[1] + height)
        self.top_right = (start_point[0] + width, start_point[1])
        self.bottom_right = (start_point[0] + width, start_point[1] + height)
        self.width = width
        self.height = height
        self.color = colors["black"]
        self.obstacles = []
        self.projectiles = []
        self.projectile_side = "right"
        self.o_size = int(self.height / 2)

    def invert_color(self):
        """
        invert lane color and obstacle color
        :returns: None
        """
        # lane
        if self.color == colors["white"]:
            self.color = colors["black"]
        elif self.color == colors["black"]:
            self.color = colors["white"]
        # obstacle
        for obstacle in self.obstacles:
            obstacle.invert_color()

    def draw(self, screen):
        """
        draws lane on pygame screen
        :param screen: the pygame suface to draw on
        :return: None
        """
        pygame.draw.line(screen, self.color, self.top_left, self.top_right, 3)
        pygame.draw.line(screen, self.color, self.bottom_left, self.bottom_right, 3)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)

    def block_lane(self):
        """
        spawn in a lane block
        if block hits player its game over
        """
        new_obstacle = Obstacle.Obstacle([self.top_right[0], self.bottom_left[1] - self.o_size], self.o_size)
        new_obstacle.color = self.color
        self.obstacles.append(new_obstacle)

    def move(self, movement, player):
        """
        move content of lane, not the lane itself
        :param movement: movement speed and direction as int
        :param player: the player object
        :returns: None
        """
        for projectile in self.projectiles:
            projectile.move(movement, player)
        for obstacle in self.obstacles:
            obstacle.move(movement, player)
            if obstacle.x < 0:
                self.obstacles.remove(obstacle)

    def add_projectile(self):
        """
        adds projectiles to the lane
        called when beats are detected
        :returns: None
        """
        if self.projectile_side == "right":
            projectile = Obstacle.Projectile((self.top_right[0], self.bottom_left[1] - self.o_size), self.o_size)
            projectile.side = self.projectile_side
            self.projectiles.append(projectile)
            self.projectile_side = "left"
        else:
            projectile = Obstacle.Projectile((self.top_left[0], self.bottom_left[1] - self.o_size), self.o_size)
            projectile.side = self.projectile_side
            self.projectiles.append(projectile)
            self.projectile_side = "right"
