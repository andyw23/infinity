"""LOADER.PY

Imports the scores.xml file and parses it into memory
"""
from utils.utils import print_format_pretty as pfp

from importer.components import Component
from importer import *
from interpreter.events import ConcertEvents


pfp("COMPONENTS CREATED",len(Component.components))

pfp("TYPES FOUND", len(Component.types))
for typ in Component.types:
    pfp("- " + typ + "S LOADED", Component.num_by_type(typ))



current_score = scores.Score.get_random_score_events()
print(current_score)
concert_events = ConcertEvents(current_score)
