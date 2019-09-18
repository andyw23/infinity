import logging, collections
from interpret.sample_events import SampleEventsGenerator

def unpack_score_events(sample_data_dict_list):
    """
    Passed a list of dicts, each containing information about a sample to be played.
    Eg. the sample.id, the corresponding Sample object, the relevant Variant, and a time_offset.

    After the score file has been read and interpreted by the importscore module, a call to the Score object will generate a sample_data_dict_list by running one of the scores..
    :param samples_list: 
    :return: dict -> concert_events
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
    # klist = list(concert_events.keys())
    # klist.sort()
    # results_list = []
    # for ky in klist:
    #     results_list.append([ky, concert_events[ky]])
    #
    # # dump
    # for lst in results_list:
    #     print("{0:08.04f}: {1:02}: {2}".format(lst[0], len(lst[1]), lst[1]))
    return concert_events
