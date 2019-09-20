import utils, pygame, logging


class Mixer():
    mixer_count = 0

    def __init__(self):
        pygame.init()
        self.soundmixer = pygame.mixer
        self.soundmixer.init()
        self.channels = []
        self.init()

    def play(self, cmnd):
        # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL

        if len([ch for ch in self.channels if ch.id == cmnd['UID']]) > 0:
            # sound is already playing
            logging.error("Cannot add {0} as it is already in a channel".format(cmnd['UID']))
        elif not self.channel_free():
            # no channels free
            logging.error("Cannot add {0} as there are no free channels".format(cmnd['UID']))
        else:
            ch = self.get_free_channel()
            ch.play_sound(cmnd)

    def set_level(self, cmnd):
        ch = self.get_channel_by_id(cmnd['UID'])
        if ch == None:
            logging.error("Cannot set the level of '{0}' as it is not found".format(cmnd['UID']))
        else:
            ch.set_level(cmnd)

    def init(self):
        for ch in self.channels:
            ch.quit()
        self.channels = []
        for i in range(utils.NUM_AUDIO_CHANNELS):
            self.channels.append(Channel(self.soundmixer, i))


    def quit(self):
        for ch in self.channels:
            ch.channel.quit()
        self.soundmixer.quit()
        pygame.quit()

    def channel_free(self):
        for ch in self.channels:
            if not ch.channel.get_busy(): return True
        return False

    def get_free_channel(self):
        for ch in self.channels:
            if not ch.channel.get_busy(): return ch
        return None

    def get_channel_by_id(self, id):
        for ch in self.channels:
            if ch.id == id: return ch
        return None

class Channel():
    def __init__(self, soundmixer, chnum):
        self.channel = soundmixer.Channel(chnum)
        self.init()

    def play_sound(self, cmnd):
        self.init()
        thissound = cmnd['SOUND']
        thissound.set_volume(cmnd['INITIAL_LEVEL'])
        self.id = cmnd['UID']
        # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL, PLAY_LENGTH
        self.channel.play(cmnd['SOUND'], cmnd['LOOP_COUNT'], cmnd['PLAY_LENGTH'], cmnd['FADE_MS'])

    def set_level(self, cmnd):
        # COMMAND, TIME, UID, LEVEL
        thissound = self.channel.get_sound()
        if thissound == None:
            logging.error("Cannot set the level of '{0}' as the sound was not found. Reinitialising the channel".format(cmnd['UID']))
            self.init()
        else:
            thissound.set_volume(cmnd['LEVEL'])

    def init(self):
        self.channel.stop()
        self.id = None

    def quit(self):
        self.init()