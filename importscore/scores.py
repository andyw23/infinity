"""SCORES.PY

Load Score objects from XML into memory
"""
import random
import logging

from importscore.components import Component
from importscore.options import Option
from interpret.concert_events import unpack_sample_events
from utils import pfp


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
        # There may be several uses of the same underlying samply in a score. Give them each a UID
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

    def get_all_scores():
        scores = Component.get_by_type(Score.component_type)
        if len(scores) == 0:
            logging.error("No scores found")
            return None
        else:
            return scores

    def get_score(arg=None):
        scores = Component.get_by_type(Score.component_type)
        if len(scores) == 0:
            logging.error("No scores found search with arg: '{0}'".format(arg))
            return None
        elif isinstance(arg, str):
            scores = [scr for scr in scores if scr.id == arg]
            if len(scores) == 0:
                logging.error("Score '{0}' not found".format(arg))
                return None
            else:
                return scores[0]
        elif isinstance(arg, int):
            if arg > len(scores):
                logging.error("Score index out of bounds. Searched for score #{0}. Only {1} scores found".format(arg, len(scores)))
            else:
                return scores[arg-1]
        else:
            return random.choice(scores)

    def get_num_scores():
        scrs = Score.get_all_scores()
        if not scrs: return None
        if len(scrs) == 0: return None
        return len(scrs)


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


def load_all_scores():
    scores = Score.get_all_scores()
    for score in scores:
        print(unpack_sample_events(score.get_sample_components()))