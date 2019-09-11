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
from interpreter.events import ConcertEvents
from utils.utils import print_format_pretty as pfp


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

current_score = scores.Score.get_random_score_events()
# print(current_score)
concert_events = ConcertEvents(current_score)

report()