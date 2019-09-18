from pydub import AudioSegment


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

        """
        If the sample file exists, proceed.
        Otherwise log the error
        """
        if self.sample_data["SAMPLE"].file_exists():
            # construct all the sample_data dicts needed to control the playing of this sample
            self.make_start_event()
        else:
            logging.error("Sample {0} file does not exist. Failed to generate audio commands")

    def get_basic_event_info(self):
        return {'TIME': self.time_offset, 'UID': self.uid, 'ID': self.sample.id}

    def make_start_event(self):
        event = self.get_basic_event_info()
        event['COMMAND'] = 'START'
        event['SOUND'] = self.get_sample_sound()
        self.sample_events.append(event)

    def get_sample_sound(self):
        # if the sample to be played is a subloop of the sample file, return the raw data that constitutes the subloop, else return the filepath of the sample - either of these can be passed to pygame.mixer.Sound() to create the sound to be played
        if self.variant.is_subloop:
            sound = AudioSegment.from_file(self.sample.filepath)
            sound = sound[self.variant.loopstarttime:self.variant.loopendtime]
            return sound.raw_data
        else:
            return self.sample.filepath

