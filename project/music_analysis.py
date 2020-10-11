import time
import pygame
import crepe
from scipy.io import wavfile
import librosa
import numpy as np

# one hand does pitch changes / one component, maybe wall etc.
#   - pitch changes shouldn't be to quick
#   - pitch changes height in viedogame, can go up and down and stuff
# one hand does beats
#   - beat dodges stuff, (not just one button)

filename = "chill.wav"


def get_pitch_change(pitch_rows):
    print(f"pitch rows: {pitch_rows}")
    li = [0]
    current = 0
    for row in pitch_rows:
        # if abs(current - row[1]) >= 200 and abs(row[0] - li[-1]) >= 1:
        if abs(current - row[1]) >= 200:
            current = row[1]
            li.append(row[0])
    return li


def play_song(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


# get pitch changes
# sr, audio = wavfile.read(filename)
# t, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=False, step_size=200)
# pitch_changes = get_pitch_change(tuple(zip(t, frequency)))
# print("pitch changes ", pitch_changes)

# get beats
"""y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beats = [round(beat, 1) for beat in librosa.frames_to_time(beat_frames, sr=sr).tolist()]
print("beats ", beats)

# play song
play_song(filename)
counter = 0
beat_counter = 0
start_time = time.time()
while time.time() - start_time < 300:
    current_time = round(time.time() - start_time, 1)
    if current_time in pitch_changes:
        pitch_changes.remove(current_time)
        counter += 1
        print(f"pitch counter: {counter}")
    if current_time in beats:
        beat_counter += 1
        beats.remove(current_time)
        print(f"beats counter {beat_counter}")"""
