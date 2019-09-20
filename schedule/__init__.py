"""

"""
import sched
import time
from play.mixer import Mixer

import pygame

_scheduler = sched.scheduler(time.time, time.sleep)
mymixer = Mixer()


def _score_end(ky, cmnd):
    # COMMAND, TIME, UID
    print("{0:10.3}: PERFORMANCE ENDS. REINITIALISING MIXER".format(ky))
    mymixer.init()

def _set_level(ky, cmnd):
    # COMMAND, TIME, UID, LEVEL
    print("{0:10.3}: LEVEL: UID: {2} LEVEL: {1}".format(ky, cmnd['LEVEL'], cmnd['UID']))
    mymixer.set_level(cmnd)


def _start_sample(ky, cmnd):
    # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL, PLAY_LENGTH
    print("{0:10.3}: START: UID: {1}: LENGTH: {2}".format(ky, cmnd['UID'], cmnd['TIME_ENDS']))
    mymixer.play(cmnd)


def schedule_command_events(command_events):
    # get a soundmixer
    # pygame.init()
    soundmixer = pygame.mixer
    soundmixer.init()

    commands = {'SCORE_END': _score_end, 'SET_LEVEL': _set_level, 'START_SAMPLE': _start_sample}
    # NB. command = 'SCORE_END', 'SET_LEVEL' and 'START_SAMPLE'
    for ky in list(command_events.keys()):
        cmnd_list = command_events[ky]
        create_concert_sounds(soundmixer, cmnd_list)
        for cmnd in cmnd_list:
            _scheduler.enter(ky, 1, commands[cmnd['COMMAND']], (ky, cmnd))


    # soundmixer.quit()
    # pygame.quit()


def create_concert_sounds(soundmixer, cmnd_list):
    # concert_event['SOUND'] is either a path to a sound file or the raw data of a sound loop
    # in either case it can be converted to a pygame Sound object. Best to do this now.
    for sample_event in cmnd_list:
        if sample_event['COMMAND'] == 'START_SAMPLE':
            sample_event['SOUND'] = soundmixer.Sound(sample_event['SOUND'])


def schedule_run():
    _scheduler.run()

# def schedule_stop():
#     _scheduler.