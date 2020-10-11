"""
module for creating all menus
like main menu

creator: Mark Jacobsen
"""
import Button
import Menu
import helper


def create_main_menu(screen_width, screen_height):
    """
    creates main menu
    :param screen_width: the width of the pygame screen
    :param screen_height: the height of the pygame screen
    :returns: Menu Object
    """
    main_menu = Menu.Menu()
    main_menu_rect = [int(screen_width/4), int(screen_height/3), int(screen_width/2), int(screen_height/10)]
    main_menu.add_button(main_menu_rect, "PLAY", helper.colors["black"])
    return main_menu
