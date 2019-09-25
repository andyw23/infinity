"""

"""
# ##############################################################################
#  Infinity. Copyright (c) 2019 Oliver Wyman Digital and Andy Wilson. This     #
#  file is subject to the terms and conditions defined in the file 'LICENSE',  #
#  which is part of this source code package.                                  #
# ##############################################################################

import logging, sched, time
from play import mixer

_scheduler = sched.scheduler(time.time, time.sleep)

class ScheduleChecker():
    def __init__(self, mixer, scheduler):
        self.mixer = mixer
        self.schedular = scheduler
        self.recentchannelsfree = []

    def check_scheduled_events(self, time, cmnd):
            evts = self.schedular.queue
            argplays = [evt for evt in evts if evt.argument[1]]
            starts = [evt for evt in argplays if evt.argument[1]['COMMAND'] == 'START_SAMPLE']
            num_starts = len(starts)
            stops = [evt for evt in argplays if evt.argument[1]['COMMAND'] == 'END_SAMPLE']
            num_chans_busy = mixer.mixer.num_channels_busy()

            # append th measure of the num_chans_busy to the recentchannelsfree list
            self.recentchannelsfree.append(num_chans_busy)
            # and if the list is more than three records long, pop the first record
            if len(self.recentchannelsfree) > 3: self.recentchannelsfree.pop(0)
            if (not num_starts and not num_chans_busy) or self.recent_chans_free_below_threshold():
                print("Nothing to play. {0} Channels busy".format(num_chans_busy))
                print("REINITIALISING")
                self.clear_scheduled_events()
                mixer.mixer.init()
            else:
                print("CH BUSY: {0}".format(num_chans_busy))

    def clear_scheduled_events(self):
        evts = self.schedular.queue
        for evt in evts: self.schedular.cancel(evt)

    def recent_chans_free_below_threshold(self):
        # if the number of channels has been low (<= 1) for three times around this check, return True
        if len(self.recentchannelsfree) < 3: return False
        for fr in self.recentchannelsfree:
            if fr > 1: return False
        return True

schedulechecker = ScheduleChecker(mixer, _scheduler)

def schedule_command_events(timeends, command_events):
    # dict to translate between the string command names passed in command_events and the actual commands to be called by the scheduler
    commands = {'SCORE_END': mixer.mixer.init,
                'SET_LEVEL': mixer.mixer.set_level,
                'START_SAMPLE': mixer.mixer.play,
                'END_SAMPLE': mixer.mixer.end}
    # NB. command = 'SCORE_END', 'SET_LEVEL' and 'START_SAMPLE'
    for ky in list(command_events.keys()):
        cmnd_list = command_events[ky]
        create_concert_sounds(cmnd_list)
        for cmnd in cmnd_list:
            _scheduler.enter(ky, 1, commands[cmnd['COMMAND']], (ky, cmnd))
            logging.info("{0:8.3}: {1}".format(ky, cmnd))

    # check on things every TIME_TO_CHECK seconds
    TIME_TO_CHECK = 5
    numchecks = int(timeends // TIME_TO_CHECK)
    for i in range(numchecks):
        ttc = i * TIME_TO_CHECK
        _scheduler.enter(ttc, 1, schedulechecker.check_scheduled_events, (ttc, None))


def create_concert_sounds(cmnd_list):
    # concert_event['SOUND'] is either a path to a sound file or the raw data of a sound loop
    # in either case it can be converted to a pygame Sound object. Best to do this now.
    for sample_event in cmnd_list:
        if sample_event['COMMAND'] == 'START_SAMPLE':
            sample_event['SOUND'] = mixer.create_sound(sample_event['SOUND'])


def schedule_run():
    _scheduler.run()

# def schedule_stop():
#     _scheduler.
