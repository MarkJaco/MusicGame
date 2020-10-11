"""
this module contains the player class
player is a figure controlled by the user

creator: Mark Jacobsen
"""

import pygame
from helper import colors


class Player:

    def __init__(self, stage, size, movement_speed, color="black"):
        self.stage = stage
        self.current_lane_index = int(len(self.stage.lanes) / 2)
        self.x = int(stage.width / 2 - size)
        self.size = size
        self.color = colors[color]
        # get lower y pos of current lane and subtract radius
        self.y = int(self.stage.lanes[self.current_lane_index].bottom_left[1] - self.size)
        # movement between lines
        self.movement_speed = movement_speed
        self.moving = 0
        self.destination_lane_index = None
        self.destination_y = None
        self.range = 200
        self.range_rect = [self.x - self.range, self.stage.lanes[0].top_left[1], self.range*2, self.stage.height]
        self.forced_lane_index = self.current_lane_index

    def invert_color(self):
        """
        invert player color
        :returns: None
        """
        if self.color == colors["white"]:
            self.color = colors["black"]
        elif self.color == colors["black"]:
            self.color = colors["white"]

    def draw(self, screen):
        """
        draws player on the pygame screen
        :param screen: the pygame screen to draw onto
        :returns: None
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        pygame.draw.rect(screen, self.color, self.range_rect, 3)

    def move_to_lane(self, lane_index):
        """
        init movement to lane
        :param lane_index: the index in stage of what lane to move to
        :return: None
        """
        if self.moving:
            print("already moving, aborting new movement")
            return
        if lane_index == self.current_lane_index:
            print("already on given lane, aborting new movement")
            return
        self.moving = -self.movement_speed if lane_index < self.current_lane_index else self.movement_speed
        self.destination_lane_index = lane_index
        self.destination_y = int(self.stage.lanes[self.destination_lane_index].bottom_left[1] - self.size)

    def reset_movement(self):
        """
        resets all variables necessary for movement
        :returns: None
        """
        self.moving = 0
        self.current_lane_index = self.destination_lane_index
        self.y = self.destination_y
        self.destination_y = None
        self.destination_lane_index = None

    def move_up(self):
        """
        moves player up one lane
        :returns: None
        """
        if self.current_lane_index == 0:
            print("already at the top, can't move upwards")
            return
        self.move_to_lane(self.current_lane_index - 1)

    def move_down(self):
        """
        moves player down one lane
        :returns: None
        """
        if self.current_lane_index == len(self.stage.lanes) - 1:
            print("already at the bottom, can't move downwards")
            return
        self.move_to_lane(self.current_lane_index + 1)

    def move(self):
        """
        gradually move player between lanes if movement is activated
        :returns: None
        """
        if self.moving > 0:
            self.y += self.moving
            if self.y >= self.destination_y:
                self.reset_movement()
        elif self.moving < 0:
            self.y += self.moving
            if self.y <= self.destination_y:
                self.reset_movement()

    def set_current_movement(self, speed):
        """
        sets current movement direction and speed
        :param speed: movement direction and speed as int
        :returns: None
        """
        self.movement_speed = int(speed)

    def move_direction(self):
        """
        move player into direction at current movement speed
        :returns: None
        """
        # dont move out of map
        if self.current_lane_index == len(self.stage.lanes) - 1 and self.movement_speed > 0:
            return
        if self.current_lane_index == 0 and self.movement_speed < 0:
            return
        # move y pos
        self.y += self.movement_speed
        # stop if hit next lane
        # up
        if self.movement_speed < 0:
            target_lane = self.stage.lanes[self.current_lane_index - 1]
            destination_y = int(target_lane.bottom_left[1] - self.size)
            if self.y <= destination_y:
                self.movement_speed = 0
                self.current_lane_index -= 1
                self.y = destination_y
        elif self.movement_speed > 0:
            target_lane = self.stage.lanes[self.current_lane_index + 1]
            destination_y = int(target_lane.bottom_left[1] - self.size)
            if self.y >= destination_y:
                self.movement_speed = 0
                self.current_lane_index += 1
                self.y = destination_y

