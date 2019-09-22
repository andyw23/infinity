import logging

import pygame

import utils

pygame.init()
_soundmixer = pygame.mixer
_soundmixer.set_num_channels(utils.NUM_AUDIO_CHANNELS)
_soundmixer.init(channels=utils.NUM_AUDIO_CHANNELS)
print(_soundmixer.get_init())


class Mixer():
    mixer_count = 0

    def __init__(self):
        self.callback = None
        self.channels = []
        for i in range(utils.NUM_AUDIO_CHANNELS):
            self.channels.append(Channel(i))

    def play(self, time, cmnd):
        # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL

        if len([ch for ch in self.channels if ch.id == cmnd['UID']]) > 0:
            # sound is already playing
            logging.error("ADD: {0}: already in a channel".format(cmnd['UID']))
        elif not self.channel_free():
            # no channels free
            str = "ADD: {0}: no free channels".format(cmnd['UID'])
            print(str)
            logging.error(str)
        else:
            str = "ADD: {0}: added".format(cmnd['UID'])
            print(str)
            logging.info(str)
            ch = self.get_free_channel()
            ch.play_sound(cmnd)

    def set_level(self, time, cmnd):
        ch = self.get_channel_by_id(cmnd['UID'])
        if not ch:
            str = "LEVEL: '{0}': not found.".format(cmnd['UID'])
            logging.error(str)
            print(str)
        else:
            ch.set_level(cmnd)
            str = "LEVEL: '{0}': Set: {1:3.3}.".format(cmnd['UID'], cmnd['LEVEL'])
            logging.error(str)
            print(str)

    def end(self, time, cmnd):
        # 'COMMAND', 'TIME', 'UID'
        ch = self.get_channel_by_id(cmnd['UID'])
        if not ch:
            str = "STOP: '{0}'. Not found.".format(cmnd['UID'])
            logging.error(str)
            print(str)
        else:
            str = "STOP: '{0}' stopped.".format(cmnd['UID'])
            logging.error(str)
            print(str)
            ch.init()

    def init(self, time=None, cmnds={}):
        print("PERFORMANCE ENDS.")
        for ch in self.channels:
            ch.init()
        # issue the callback command, to be trapped by the main app
        if self.callback: self.callback()

    def channel_free(self):
        for ch in self.channels:
            if not ch.channel.get_busy(): return True
        return False

    def get_free_channel(self):
        for ch in self.channels:
            if not ch.channel.get_busy(): return ch
        return None

    def num_free_channels(self):
        return len([ch for ch in self.channels if not ch.id])

    def num_used_channels(self):
        return len([ch for ch in self.channels if ch.id])

    def num_channels_busy(self):
        return len([ch for ch in self.channels if ch.channel.get_busy()])

    def get_channel_by_id(self, id):
        for ch in self.channels:
            if ch.id == id: return ch
        return None

    def get_volumes(self):
        for i in range(len(self.channels)):
            ch = self.channels[i]
            print("{0:02}: {1}: CHV: {1:06.2}: SOV: {2:06.2}".format(i, ch.id, ch.channel.get_volume(), ch.channel.sound.get_volume()))

class Channel():
    def __init__(self, chnum):
        self.channelnum = chnum
        self.channel = _soundmixer.Channel(chnum)
        self.channel.set_volume(1.0)
        self.init()

    def play_sound(self, cmnd):
        self.init()
        thissound = cmnd['SOUND']
        thissound.set_volume(self.get_trimmed_level(cmnd['INITIAL_LEVEL']))
        self.id = cmnd['UID']
        # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL, PLAY_LENGTH
        lc = cmnd['LOOP_COUNT']
        pl = cmnd['PLAY_LENGTH']
        fd = cmnd['FADE_MS']

        self.channel.play(thissound, lc, pl, fd)

    def set_level(self, cmnd):
        # COMMAND, TIME, UID, LEVEL
        thissound = self.channel.get_sound()
        if not thissound:
            logging.error("Cannot set the level of '{0}' as the sound was not found. Reinitialising the channel".format(
                cmnd['UID']))
            self.init()
        else:
            thissound.set_volume(self.get_trimmed_level(cmnd['LEVEL']))

    def get_trimmed_level(self, level):
        thissound = self.channel.get_sound()
        if level < 0.3: level = 0.3
        return level

    def init(self):
        self.channel.fadeout(1000)
        self.id = None

    def quit(self):
        self.init()


"""
CREATE THE MIXER THAT WILL BE USED THROUGHOUT
"""
mixer = Mixer()


def create_sound(snd_src):
    # snd_src is either a path to a sound file or the raw data of a sound loop
    # in either case it can be converted to a pygame Sound object.
    return _soundmixer.Sound(snd_src)


def quit_pygame():
    if _soundmixer != None: _soundmixer.quit()
    pygame.quit()
