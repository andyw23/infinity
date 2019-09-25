# ##############################################################################
#  Infinity. Copyright (c) 2019 Oliver Wyman Digital and Andy Wilson. This     #
#  file is subject to the terms and conditions defined in the file 'LICENSE',  #
#  which is part of this source code package.                                  #
# ##############################################################################

import logging, collections
from interpret.sample_events import SampleEventsGenerator
from play.mixer import mixer


def unpack_sample_events(sample_data_dict_list):
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
    else:
        score_time_ends = 0
        for sample_data_dict in sample_data_dict_list:
        # Caluclate the associated events to control this sample
        # The associated sample_data is passed to the SampleEventsGenerator object to be unpacked
        # The events associated with the sample are then appended to the local concert_events variable
            sample_events = SampleEventsGenerator(sample_data_dict).sample_events
            # every sample_events list has a dict member with the TIME_ENDS key set to the time the sample ends (length of playback + time_offset)
            sample_time_ends = [se for se in sample_events if 'TIME_ENDS' in list(se.keys())][0]['TIME_ENDS']
            # if this sample's 'TIME_ENDS' is greater than the current score_time_ends, update the latter
            if sample_time_ends > score_time_ends: score_time_ends = sample_time_ends

            # group events by timing - put all events with the same timing into the same list within the concert_events dict, with the timing as the key
            for evt in sample_events:
                if evt['TIME'] in concert_events.keys():
                    concert_events[evt['TIME']].append(evt)
                else:
                    concert_events[evt['TIME']] = [evt]
                evt.pop('TIME', None)

        score_time_ends = round(score_time_ends, 3)
        score_end_event = {'TIME': score_time_ends, 'COMMAND': 'SCORE_END'}
        if score_time_ends in concert_events.keys():
            concert_events[score_time_ends].append(score_end_event)
        else:
            concert_events[score_time_ends] = [score_end_event]
        timeends = score_end_event['TIME']

        # Report how long the score will play
        mins = int(timeends // 60)
        secs = int((timeends) - (mins * 60))
        msss = int((timeends % 1) * 1000)
        print("PERFORMANCE ENDS: {0:3}:{1:2}:{2:3}".format(mins, secs, msss))
    return timeends, concert_events

def log_command_events(command_events):
    for ky in command_events.keys():
        for cevent in command_events[ky]:
            sound = type(cevent['SOUND']) if 'SOUND' in cevent.keys() else 'False'
            logging.info("TIME: {0: 8.04}   UID: {1:30} COMMAND: {2:6} SOUND: {3}".format(ky, cevent['UID'], cevent['COMMAND'], sound))