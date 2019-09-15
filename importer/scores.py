"""SCORES.PY

Load Score objects from XML into memory
"""
import random
import logging

from importer.components import Component
from importer.options import Option


class Score(Component):
    component_type = 'SCORE'
    elements_str = ".//score"

    def get_elements():
        return Component.get_elements(Score.elements_str)

    def get_random_score():
        if not Component.has_type(Score.component_type):
            logging.error("No Scores found among the components")
        else:
            return random.choice(Component.get_by_type(Score.component_type))

    def get_random_score_events():
        return Score.get_random_score().get_events()

    def get_all_scores():
        scores = Component.get_by_type(Score.component_type)
        if len(scores) == 0:
            logging.error("No scores found")
        else:
            return scores

    def __init__(self, score):
        self.component_type = Score.component_type
        self.id = score.get("id").upper()
        self.create_element = score.find("./create")
        self.create_option = Component.get_option_from_element(self, self.create_element)
        self.create_id = self.create_element.get("id").upper()

    def get_events(self):
        """
        Retrieves all the events invoked by this score
        :return: List
        """
        obj = Component.get_component_by_id(self.create_id)
        obj = Component.get_component_by_id(obj.id)
        # pass the starting time (0.0) and
        return obj.get_events(time_offset=0.0, variant_id=None)
