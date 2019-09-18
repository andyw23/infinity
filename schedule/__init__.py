"""

"""
import sched
import time
import pygame

_scheduler = sched.scheduler(time.time, time.sleep)

def schedule_command_events(command_events):
    # get a soundmixer
    pygame.init()
    soundmixer = pygame.mixer
    soundmixer.init()

    for ky in list(command_events.keys()):
        cmnd_list = command_events[ky]
        create_concert_sounds(soundmixer, cmnd_list)
        for cmnd in cmnd_list:
            _scheduler.enter(ky, 1, _print_command, (ky, cmnd))
    soundmixer.quit()
    pygame.quit()

def create_concert_sounds(soundmixer, cmnd_list):
    # concert_event['SOUND'] is either a path to a sound file or the raw data of a sound loop
    # in either case it can be converted to a pygame Sound object. Best to do this now.
    for sample_event in cmnd_list:
        if sample_event['COMMAND'] == 'START':
            sample_event['SOUND'] = soundmixer.Sound(sample_event['SOUND'])

def schedule_run():
    _scheduler.run()

def _print_command(ky, cmnd):
    print("{0:7.3}: {1}".format(ky, cmnd))