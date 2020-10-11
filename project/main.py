import pygame
import helper
import Stage
import Player
import LevelBuilder
import ast
import pathlib
import menu_creation


class Main:

    def __init__(self):
        # game init
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        # general init
        self.running = True
        self.seen_timestamps = set()
        self.background_color = helper.colors["white"]
        self.particles = []
        self.level = None
        self.projectile_movement = 0.7
        self.test = []

        # custom objects
        self.stage = Stage.Stage((0, 100), self.screen.get_width(), self.screen.get_height()/2, 5)
        self.player = Player.Player(self.stage, int(self.stage.lanes[0].height/4), 0)

        # menus
        self.main_menu = menu_creation.create_main_menu(self.screen.get_width(), self.screen.get_height())
        self.active_menu = self.main_menu

    def invert_colors(self):
        """
        inverts colors of all stage objects (lanes, etc.)
        and player color
        """
        self.player.invert_color()
        self.stage.invert_color()
        if self.background_color == helper.colors["white"]:
            self.background_color = helper.colors["black"]
        elif self.background_color == helper.colors["black"]:
            self.background_color = helper.colors["white"]

    def draw(self):
        """
        draws everything on screen (nodes, connections etc.)
        :returns: None
        """
        # menu
        if self.active_menu:
            # general menu draw
            self.active_menu.draw(self.screen)
            return
        # actual game
        self.stage.draw(self.screen)
        self.player.draw(self.screen)
        for particle in self.particles:
            particle.draw(self.screen)

    def move(self, dt):
        """
        handles all movement of all objects
        :param dt: delta time for constant fps
        :returns: None
        """
        if self.active_menu:
            return
        self.player.move_direction()
        self.stage.move(-self.projectile_movement * dt, self.player)
        for particle in self.particles:
            particle.move()

        # intersection
        for lane in self.stage.lanes:
            # big obstacles
            for obstacle in lane.obstacles:
                if obstacle.intersects_player(self.player):
                    print(f"intersected with {obstacle}")
                    self.running = False
            # small projectiles
            for projectile in lane.projectiles:
                if projectile.intersects_player(self.player):
                    print(f"intersected with {projectile}")
                    self.running = False

    def create_obstacles(self, current_time):
        """
        creates obstacles at correct timestamp
        :param current_time: the current time rounded to 1
        :returns: None
        """
        if current_time in self.level and current_time not in self.seen_timestamps:
            # projectiles
            if self.level[current_time][0]:
                self.stage.lanes[self.player.current_lane_index].add_projectile()
            # obstacles
            if self.level[current_time][1]:
                new_lane_index = self.player.forced_lane_index + self.level[current_time][1]
                # hit border
                if new_lane_index > len(self.stage.lanes) - 1 or new_lane_index < 0:
                    new_lane_index = self.player.forced_lane_index - self.level[current_time][1]
                # block lanes
                for obstacle_lane in range(len(self.stage.lanes)):
                    if not obstacle_lane == new_lane_index:
                        self.stage.lanes[obstacle_lane].block_lane()
                self.player.forced_lane_index = new_lane_index
            # don't do again
            self.seen_timestamps.add(current_time)

    def change_colors(self, current_time):
        """
        change stage colors at specific points in time
        (usually moments of highest amplitude)
        :param current_time: the current time rounded to 1
        :returns: None
        """
        if current_time in self.level["color_changes"] and current_time not in self.seen_timestamps:
            self.invert_colors()

    def activate_game(self, song_name):
        """
        closes current menu and activates game
        :param song_name: the name of the song to play the level with
        :returns: None
        """
        # build level
        music_name = f"music/{song_name}"
        music_file = f"{music_name}.wav"
        level_file = f"{music_name}.txt"
        level_builder = LevelBuilder.LevelBuilder()
        num_steps = self.screen.get_width() - self.player.x - self.player.range - 150
        projectile_speed = self.projectile_movement
        file_exists = pathlib.Path(level_file).is_file()
        if file_exists:
            with open(level_file) as f:
                for line in f:
                    self.level = ast.literal_eval(line)
                    # check if same as last time
                    if not num_steps == self.level["projectile_distance"] or \
                            not projectile_speed == self.level["projectile_speed"]:
                        file_exists = False
        if not file_exists:
            self.level = level_builder.build_level(music_file, projectile_speed, num_steps)
            # write level to file
            level_f = open(level_file, "w")
            level_f.write(str(self.level))
            level_f.close()
        print(f"built level {self.level}")
        self.active_menu = None
        helper.play_song(music_file)

    def handle_menu_events(self, events):
        """
        handles events regarding the menu
        such as clicking buttons
        :param events: all current events
        :returns: None
        """
        button = ""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                button = self.active_menu.button_clicked(x, y)
        # handle different buttons
        if button.lower() == "play":
            self.activate_game("chill")

    def handle_game_events(self, events, dt):
        """
        handle events regarding the gameplay
        such as keyboard events
        :param events: all current events
        :param dt: delta t, time since last called in ms
        :returns: None
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # modify speed according to length of pitch change
                    self.player.set_current_movement(0.5 * dt)
                elif event.key == pygame.K_UP:
                    self.player.set_current_movement(-0.5 * dt)
                elif event.key == pygame.K_RIGHT:
                    for lane in self.stage.lanes:
                        for projectile in lane.projectiles:
                            if 0 < projectile.x - self.player.x < self.player.range:
                                self.particles.append(projectile.destroy())
                                lane.projectiles.remove(projectile)
                elif event.key == pygame.K_LEFT:
                    for lane in self.stage.lanes:
                        for projectile in lane.projectiles:
                            if 0 < self.player.x - (projectile.x + projectile.size) < self.player.range:
                                self.particles.append(projectile.destroy())
                                lane.projectiles.remove(projectile)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.set_current_movement(0)
                elif event.key == pygame.K_UP:
                    self.player.set_current_movement(0)

    def handle_events(self, dt):
        """
        handle events such as key presses
        :param dt: time since last call
        :returns: None
        """
        events = pygame.event.get()
        # general
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        # menu
        self.handle_menu_events(events)
        # game
        self.handle_game_events(events, dt)

    def run(self):
        """
        method to call if starting up
        contains main loop
        returns: None
        """
        while self.running:
            # constant fps
            dt = self.clock.tick(120)

            # keep track of time
            if not self.active_menu:
                current_time = helper.current_song_time()
                self.change_colors(current_time)
                self.create_obstacles(current_time)

            # events
            self.handle_events(dt)

            # movement
            self.move(dt)

            # draw
            self.screen.fill(self.background_color)
            self.draw()
            pygame.display.flip()
        print(helper.current_song_time())


if __name__ == "__main__":
    main = Main()
    main.run()
