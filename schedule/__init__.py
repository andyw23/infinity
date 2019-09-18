"""

"""
import sched
import time

_scheduler = sched.scheduler(time.time, time.sleep)

def schedule_command_events(concert_events):
    for ky in list(concert_events.keys()):
        cmnd_list = concert_events[ky]
        for cmnd in cmnd_list:
            _scheduler.enter(ky, 1, _print_command, (ky, cmnd))

def schedule_run():
    _scheduler.run()

def _print_command(ky, cmnd):
    print("{0:7.3}: {1}".format(ky, cmnd))