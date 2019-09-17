import logging, collections


def unpack_concert_events(sample_data_dict_list):
    """
    Passed a list of dicts, each containing information about a sample to be played.
    Eg. the sample.id, the corresponding Sample object, the relevant Variant, and a time_offset
    :param samples_list: 
    :return: 
    """
    concert_events = {}
    if len(sample_data_dict_list) == 0:
        logging.critical("Samples dictionary is empty")
    for sample_data_dict in sample_data_dict_list:
    # Caluclate the associated events to control this sample
    # The associated sample_data is passed to the SampleEventsGenerator object to be unpacked
    # The events associated with the sample are then appended to the local concert_events variable
        sample_events = SampleEventsGenerator(sample_data_dict).sample_events
        # group events by timing - put all events with the same timing into the same list within the concert_events dict, with the timing as the key
        for evt in sample_events:
            if evt['TIME'] in concert_events.keys():
                concert_events[evt['TIME']].append(evt)
            else:
                concert_events[evt['TIME']] = [evt]
            evt.pop('TIME', None)

    # order the dict
    klist = list(concert_events.keys())
    klist.sort()
    results_list = []
    for ky in klist:
        results_list.append([ky, concert_events[ky]])

    # dump
    for lst in results_list:
        print("{0:08.04f}: {1:02}: {2}".format(lst[0], len(lst[1]), lst[1]))
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

        # TODO: NOTE ON TIMING: Timings are currently rounded twice during execution - to four places in importer.samples.get_sample_components, and then again here, to three place - enough to calculate timings in 0.1 milliseconds
        self.time_offset = round(sample_data['TIME_OFFSET'], 3)

        """
        If the sampel file exists, proceed.
        Otherwise log the error
        """
        if self.sample_data["SAMPLE"].file_exists():
            self.make_start_event()
        else:
            logging.error("Sample {0} file does not exist. Failed to generate audio commands")

    def make_start_event(self):
        event = {'TIME': self.time_offset}
        event['TYPE'] = 'START'
        sample = self.sample_data['SAMPLE']
        variant = self.sample_data['VARIANT']
        event['ID'] = sample.id
        event['FILENAME'] = sample.filename
        event['FILEPATH'] = sample.filepath
        self.sample_events.append(event)
