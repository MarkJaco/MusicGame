"""
module contains stage module
sets the main stage for the game
contains multiple lanes

creator: Mark Jacobsen
"""

import pygame
import Lane


class Stage:

    def __init__(self, start_point, width, height, lane_amount=5):
        self.start_point = start_point
        self.width = width
        self.height = height
        self.lane_amount = lane_amount
        self.lanes = self.make_lanes()

    def invert_color(self):
        """
        invert stage color
        meaning all the lanes
        :returns: None
        """
        for lane in self.lanes:
            lane.invert_color()

    def make_lanes(self):
        """
        make all lanes
        :returns: all lane objects as list
        """
        lanes = []
        current_point = self.start_point
        for x in range(self.lane_amount):
            current_lane = Lane.Lane(current_point, self.width, self.height / self.lane_amount)
            lanes.append(current_lane)
            current_point = [current_point[0], current_point[1] + self.height / self.lane_amount]
        return lanes

    def draw(self, screen):
        """
        draw all lanes --> the stage on pygame screen
        also draws range rect
        :param screen: the pygame screen
        :returns: None
        """
        for lane in self.lanes:
            lane.draw(screen)

    def move(self, movement, player):
        """
        move content of all lanes
        :param movement: movement speed and direction as int
        :param player: the player object
        :returns: None
        """
        for lane in self.lanes:
            lane.move(movement, player)
