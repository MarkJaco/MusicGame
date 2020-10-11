"""
module contains helper functions / variables for 
TerminalStrategyMaker project
"""
import pygame.mixer

colors = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
         "yellow": (255, 255, 0), "grey": (105, 105, 105), "white": (255, 255, 255),
         "black": (0, 0, 0), "orange": (255, 69, 0)}


def play_song(path):
    """
    play given song with pygame
    :param path: the path to the music file
    :returns: None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def current_song_time():
    """
    get the current timstamp of the song being played
    :returns: timestamp of song in seconds rounded
    """
    return round(pygame.mixer.music.get_pos() / 1000, 1)
