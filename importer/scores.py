"""SCORES.PY

Load Score objects from XML into memory
"""
import random

from importer.components import Component
from importer.options import Option


class Score(Component):
    type = 'SCORE'
    elements_str = ".//score"

    def get_elements():
        return Component.get_elements(Score.elements_str)

    def get_random_score():
        if not Component.has_type(Score.type):
            print("ERROR: NO SCORES AMONG COMPONENTS")
        else:
            return random.choice(Component.get_by_type(Score.type))

    def get_random_score_events():
        return Score.get_random_score().get_events()

    def __init__(self, score):
        self.type = Score.type
        self.id = score.get("id").upper()
        self.create_element = score.find("./create")
        self.create_options = Component.get_option_from_element(self.create_element)
        self.create_id = self.create_element.get("id").upper()

    def get_events(self):
        """
        Retrieves all the events invoked by this score
        :return: List
        """
        obj = Component.get_component_by_id(self.create_id)
        obj = Component.get_component_by_id(obj.id)
        return obj.get_events(self.create_options)

"""
LOAD ALL SCORES
"""
Component.load_type_objects(Score)
