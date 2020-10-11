"""
module contains LevelBuilder class
LevelBuilder builds a game level by analysing the given music

creator: Mark Jacobsen
"""
import time
import pygame
import crepe
from scipy.io import wavfile
import librosa


class LevelBuilder:

    def __init__(self):
        pass

    @staticmethod
    def calculate_projectile_time(projectile_speed, projectile_distance):
        """
        calculate the amount of time the projectile needs to reach player
        :param projectile_speed: the speed of flying projectiles
        :param projectile_distance: the distance the projectile needs to travel, to get to player
        :returns: amount of time as double (1 = 1 millisecond)
        """
        return (projectile_distance / projectile_speed) / 1000

    @staticmethod
    def generate_projectile_list(beat_list, projectile_time):
        """
        generates list of projectiles
        :param beat_list: the list of beats [time_beat1, time_beat1, ...]
        :param projectile_time: the amount of time a projectile needs to reach the player
        :returns: [time_projectile1, time_projectile2, ...]
        """
        return list(map(lambda t: round(t - projectile_time, 1), beat_list))

    @staticmethod
    def generate_beat_list(music_file):
        """
        gets all timestamps of beats in song
        :param music_file: the music file to analyse
        :returns: [time_beat1, time_beat2, ...]
        """
        y, sr = librosa.load(music_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        detected_beats = librosa.frames_to_time(beat_frames, sr=sr).tolist()
        beats = [round(beat, 1) for beat in detected_beats]
        return beats

    @staticmethod
    def get_pitch_rows(music_file, step_size=200):
        """
        gets pitch on different times in music
        :param music_file: the path to music file
        :param step_size: how often to check for pitch
        :returns: pitch_list [[time, frequency], [...]]
        """
        sr, audio = wavfile.read(music_file)
        t, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=False, step_size=step_size)
        return tuple(zip(t, frequency))

    @staticmethod
    def get_pitch_changes(pitch_rows):
        """
        gets pitch changes in music
        :param pitch_rows: the path to the music file
        :returns: [[timestamp, frequency], [...]]
        """
        li = [[0, 0]]
        current = 0
        for row in pitch_rows:
            # if abs(current - row[1]) >= 200:
            if abs(current - row[1]) >= 200 and abs(row[0] - li[-1][0]) >= 1:
                current = row[1]
                li.append(row)
        return li

    @staticmethod
    def generate_obstacles(pitch_changes):
        """
        generates locations and times to place obstacles
        :param pitch_changes: the changes in pitch of the song [[time, new_frequency], [...]]
        :returns: {timestamp: -1 or +1}
        """
        obstacles = {}
        previous = float("inf")
        for change in pitch_changes:
            # higher pitch --> move up
            if change[1] > previous:
                operation = -1
                previous = change[1]
            # lower pitch --> move down
            else:
                operation = 1
                previous = change[1]
            obstacles[change[0]] = operation
        return obstacles

    def get_highest_amplitude(self, music_file):
        """
        gets highest amplitude from song
        :param music_file: the path to the music file
        :returns: [a1, a2, etc.] as set
        """
        y, sr = librosa.load(music_file)
        m = y.max()
        highest_points = set()
        for c, p in enumerate(y):
            if abs(p) > m - 0.01:
                t = round(c / sr, 1)
                highest_points.add(t)
        return highest_points

    def build_level(self, music_file, projectile_speed, projectile_distance, beat_list=None, pitch_changes=None, highest_amplitude=None):
        """
        build level from music file
        :param music_file: the path to the music file
        :param projectile_speed: the speed of flying projectiles
        :param projectile_distance: the distance the projectile needs to travel, to get to player
        :param beat_list: the list of beats if humanly detected (optional)
        :param pitch_changes: the changes in the pitch [[time, frequency], [...]](optional)
        :returns: Level as dict of instructions {"timestamp": [Boolean Projectile, obstacle lane_change as num]]}
        """
        print("generating projectiles...")
        projectile_time = self.calculate_projectile_time(projectile_speed, projectile_distance)
        beat_list = self.generate_beat_list(music_file) if not beat_list else beat_list
        projectile_list = self.generate_projectile_list(beat_list, projectile_time)
        if not pitch_changes:
            print("generating obstacles...")
            pitch_rows = self.get_pitch_rows(music_file, 200)
            pitch_changes = self.get_pitch_changes(pitch_rows)
        obstacles = self.generate_obstacles(pitch_changes)
        print("finding highest amplitudes...")
        highest_amplitude = self.get_highest_amplitude(music_file) if not highest_amplitude else highest_amplitude

        # generate dictionary
        return_d = {}
        time_stamp = 0
        while time_stamp < projectile_list[-1]:
            rounded_time_stamp = round(time_stamp, 1)
            return_d[rounded_time_stamp] = [False, 0]
            if rounded_time_stamp in projectile_list:
                return_d[rounded_time_stamp][0] = True
            if rounded_time_stamp in obstacles:
                return_d[rounded_time_stamp][1] = obstacles[rounded_time_stamp]
            time_stamp += 0.1
        return_d["color_changes"] = highest_amplitude
        return_d["projectile_speed"] = projectile_speed
        return_d["projectile_distance"] = projectile_distance
        return return_d
