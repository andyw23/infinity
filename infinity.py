"""infinity.py
Andy Wilson, 2019
Imports the scores.xml file and parses it into memory
This is not invoked explicitly but happens automatically when the modules are imported
"""
import logging
logging.basicConfig(
    filename='import.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(msecs)03d: %(levelname)s: %(module)s: %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from importscore.scores import Score
from importscore.samples import Sample
from importscore import components
from importscore import load_components, score_is_valid
from interpret.concert_events import *
from utils import pfp
from schedule import schedule_command_events, schedule_run


def load_all_scores():
    scores = Score.get_all_scores()
    for score in scores:
        print(unpack_score_events(score.get_sample_components()))

def dump_score_events(sample_events):
    """
    prints out each individual event
    :param sample_events: list - a list of events
    """
    for sample_event in sample_events:
        print("-------------------------------------------")
        pfp("SAMPLE", sample_event["SAMPLE"].id)
        pfp("VARIANT", sample_event["VARIANT"].id)
        pfp("TIME OFFSET", sample_event["TIME_OFFSET"])


# load_score_text()

print(score_is_valid())

load_components()
components.log_components_loaded()
score = Score.get_score()
if score != None:
    print("Score '{0}' retrieved".format(score.id))
    sample_events = score.get_sample_components()
    # Sample.log_sample_events(sample_events)
    command_events = unpack_score_events(sample_events)
    # log_command_events(command_events)
    schedule_command_events(command_events)
    schedule_run()