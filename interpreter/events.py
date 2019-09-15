import logging


def unpack_concert_events(sample_data_dict_list):
    """
    Passed a list of dicts, each containing information about a sample to be played.
    Eg. the sample.id, the corresponding Sample object, the relevant Variant, and a time_offset
    :param samples_list: 
    :return: 
    """
    concert_events = []
    if len(sample_data_dict_list) == 0:
        logging.critical("Samples dictionary is empty")
    for sample_data_dict in sample_data_dict_list:
        # Caluclate the associated events to control this sample
        # The associated sample_data is passed to the SampleEventsGenerator object to be unpacked
        # The events associated with the sample are then appended to the local concert_events variable
        concert_events += SampleEventsGenerator(sample_data_dict).sample_events
    return concert_events


class SampleEventsGenerator():
    """
    Class to generate all the relevant events for a sample, commands to start and stop the playing of the sample at the appropriate tiems, and to loop the sample and change its level as appropriate.

    The events are generated during initialisation, and added to the Object sample_events property.
    """
    def __init__(self, sample_data):
        """
        On __init__ the sample data is analysed to create sample events
        :param sample_data: dict - data asscoiated with a sample: the sampel object itself, the selected variant data, and timeing info.
        """
        # sample_data_dict is a dictionary containing a Sample object at the key 'SAMPLE'
        # A Variant object at the key 'VARIANT'
        # A time offset value at 'TIME_OFFSET'
        self.sample_events = []
        self.sample_data = sample_data
        self.time_offset = sample_data['TIME_OFFSET']

    def make_start_event(self):
        event = {'TIME': self.time_offset}
        event['TYPE'] = 'START'
        sample = self.sample_data['SAMPLE']
        variant = self.sample_data['VARIANT']
        event['ID'] = sample.id
        event['FILENAME'] = sample.file + '.wav'
        self.sample_events.append(event)

