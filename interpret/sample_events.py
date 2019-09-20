from pydub import AudioSegment

from utils import FADE_TIME


class SampleEventsGenerator():
    """
    Class to generate all the relevant events for a sample, commands to start and stop the playing of the sample at the appropriate tiems, and to loop the sample and change its level as appropriate.

    The events are generated during initialisation, and added to the Object sample_events property.
    """

    def __init__(self, soundmixer, sample_data):
        """
        On __init__ the sample data is analysed to create sample events
        :param sample_data: dict - data asscoiated with a sample: the sampel object itself, the selected variant data, and timeing info.
        """
        # sample_data_dict is a dictionary containing a Sample object at the key 'SAMPLE'
        # A Variant object at the key 'VARIANT'
        # A time offset value at 'TIME_OFFSET'
        self.sample_events = []
        self.sample_data = sample_data
        self.sample = self.sample_data['SAMPLE']
        self.variant = self.sample_data['VARIANT']
        self.uid = self.sample_data['UID']
        # TODO: NOTE ON TIMING: Timings are currently rounded twice during execution - to four places in importscore.samples.get_sample_components, and then again here, to three place - enough to calculate timings in 0.1 milliseconds
        self.time_offset = round(sample_data['TIME_OFFSET'], 3)
        self.playlength = 0

        # calculate when this sample ends
        # loopcount 0 -> loop until looplength
        if self.variant.loopcount == 0:
            self.playlength = self.variant.looplength
        elif self.variant.loopcount == None:
            self.playlength = self.variant.loopsamplelength
        else:
            self.playlength = self.variant.loopcount * self.variant.loopsamplelength

        # calculate when the sample will stop playing - adding the time_offset to the playlength
        # NB. playlength is in mS
        self.timeends = round((self.time_offset + (self.playlength / 1000)), 4)

        """
        If the sample file exists, proceed.
        Otherwise log the error
        """
        if self.sample_data["SAMPLE"].file_exists():
            # construct all the sample_data dicts needed to control the playing of this sample
            self.make_start_event()
            if len(self.variant.dynamics) > 0:
                self.make_dynamics_events()
        else:
            logging.error("Sample {0} file does not exist. Failed to generate audio commands")

    def get_basic_event_info(self):
        return {'TIME': self.time_offset, 'UID': self.uid}

    def make_start_event(self):
        event = self.get_basic_event_info()
        event['COMMAND'] = 'START_SAMPLE'
        event['LOOP_LENGTH'] = self.variant.looplength

        # in the score, loopcount 0 means play until told to stop, whereas in pygame that is a loopcount of -1.
        # in the score, a loopcount > 0 determines how many times to play the loop, in loopgame the loop plays (loopcount + 1) times
        event['LOOP_COUNT'] = (self.variant.loopcount - 1)

        event['FADE_MS'] = FADE_TIME
        event['SOUND'] = self.get_sample_sound()
        event['TIME_ENDS'] = self.timeends

        # in the score, levels are 0-255, in pygame they are 0.0-1.0
        event['INITIAL_LEVEL'] = round((self.variant.initial_level / 255), 3)
        event['PLAY_LENGTH'] = self.playlength
        self.sample_events.append(event)

    def make_dynamics_events(self):
        if self.variant.has_dynamics():
            for inst_key in self.variant.dynamics.keys():
                if inst_key != 0.0:
                    inst = self.variant.dynamics[inst_key]
                    event = self.get_basic_event_info()
                    event['COMMAND'] = 'SET_LEVEL'
                    event['TIME'] = round(self.time_offset + inst.time, 3)
                    # in the score, levels are 0-255, in pygame they are 0.0-1.0
                    event['LEVEL'] = round((inst.level / 255), 3)
                    self.sample_events.append(event)

    def get_sample_sound(self):
        # if the sample to be played is a subloop of the sample file, return the raw data that constitutes the subloop, else return the filepath of the sample - either of these can be passed to pygame.mixer.Sound() to create the sound to be played
        if self.variant.is_subloop:
            sound = AudioSegment.from_file(self.sample.filepath)
            sound = sound[self.variant.loopstarttime:self.variant.loopendtime]
            return sound.raw_data
        else:
            return self.sample.filepath
