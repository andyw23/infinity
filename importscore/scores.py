"""SCORES.PY

Load Score objects from XML into memory
"""
import random
import logging

from importscore.components import Component
from importscore.options import Option


class Score(Component):
    component_type = 'SCORE'
    elements_str = ".//score"

    def __init__(self, score):
        self.component_type = Score.component_type
        self.id = score.get("id").upper()
        self.create_element = score.find("./create")
        self.create_option = Component.get_option_from_element(self, self.create_element)
        self.create_id = self.create_element.get("id").upper()

    def get_sample_components(self):
        """
        Retrieves all the sample components invoked by this score. The sample components relating to a score are in a dict that contains the sample component itself, the relevant variant and some offset timing information. This info is later used by the interpreter to produce commands to drive the audio engine.

        :return: List
        """
        obj = Component.get_component_by_id(self.create_id)
        obj = Component.get_component_by_id(obj.id)
        # pass the starting time (0.0), None for the variant, and initialise the depth to 1
        sample_components = obj.get_sample_components(time_offset=0.0, variant_id=None, depth=1)
        # before returning, as the same sample may be invoked several times by the same score, each invokation needs a unique id
        ids = []
        for sample_component in sample_components:
            id = sample_component['SAMPLE'].id
            ids.append(id)
            sample_component['UID'] = "{0}{1:04d}".format(id, ids.count(id))
        return sample_components

    """
    CLASS METHODS
    """
    def get_elements():
        return Component.get_elements(Score.elements_str)

    def get_random_score():
        if not Component.has_type(Score.component_type):
            logging.error("No Scores found among the components")
        else:
            return random.choice(Component.get_by_type(Score.component_type))

    def get_random_score_sample_components():
        return Score.get_random_score().get_sample_components()

    def get_all_scores():
        scores = Component.get_by_type(Score.component_type)
        if len(scores) == 0:
            logging.error("No scores found")
        else:
            return scores