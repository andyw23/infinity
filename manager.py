"""manager.py
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
# ^([^\[]+)(\[[\s\d]+])\s*(\w*)\s*-\s*(\S*)\s*-(.+)$
from importer import *
from importer.components import Component
# from importer import components
from interpreter.events import *
from importer.scores import Score
from utils import pfp


def report():
    """
    Writes a brief report on the import process
    :return: None
    """
    print("------------------------------")
    pfp("COMPONENTS CREATED", len(Component.components))
    pfp("TYPES FOUND", Component.num_component_types)
    for typ in Component.component_types:
        pfp("- " + typ + "S LOADED", Component.num_by_type(typ))
    print("------------------------------")


def load_all_components():
    """
    Loads all of the Choose, Concert, Score and Sample components.
    These then exist int he dictionary Component.components, with the IDs as the keys
    :return: None
    """
    Component.load_type_objects(samples.Sample)
    Component.load_type_objects(choices.Choice)
    Component.load_type_objects(concerts.Concert)
    Component.load_type_objects(scores.Score)


def load_all_scores():
    scores = Score.get_all_scores()
    for score in scores:
        print(unpack_concert_events(score.get_events()))

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

def xml_is_valid():
    import xmlschema
    schema = xmlschema.XMLSchema('scores.xsd')
    print(schema.is_valid('scores.xml'))

load_all_components()
report()
events = Score.get_random_score_events()
# dump_score_events(events)
unpack_concert_events(events)
# print(concert_events)


