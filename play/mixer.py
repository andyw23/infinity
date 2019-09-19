class Mixer():
    mixer_count = 0

    def __init__(self):
        self.channels = {}
        pygame.init()
        self.soundmixer = pygame.mixer
        self.soundmixer.init()

    def play(self, cmnd):
        # COMMAND, TIME, UID, LOOP_LENGTH, LOOP_COUNT, FADE_MS, SOUND, TIME_ENDS, INITIAL_LEVEL

        if cmnd['UID'] in self.channels.keys():
            logging.error("Cannot add {0} as it is already in a channel".format(cmnd['UID']))
        else:
            thissound = cmnd['SOUND']
            self.channels[cmnd['UID']] = thissound

    def quit(self):
        for snd in self.channels:
            snd.stop()
        self.soundmixer.quit()
        pygame.quit()