__all__ = ['choices','concerts','samples','scores']

from importscore import *
from importscore.components import Component
from utils import SCHEMA_FILENAME, SCORE_FILENAME

def load_components():
    """
    Loads all of the Choose, Concert, Score and Sample components. These then exist in the dictionary Component.components, with the IDs as the keys
    :return: None
    """
    Component.load_type_objects(samples.Sample)
    Component.load_type_objects(choices.Choice)
    Component.load_type_objects(concerts.Concert)
    Component.load_type_objects(scores.Score)


def score_is_valid():
    """
    Checks whether the scores XML file validates against the correspondingly named XSD file
    :return: Boolean
    """
    import xmlschema
    schema = xmlschema.XMLSchema(SCHEMA_FILENAME)
    return schema.is_valid(SCORE_FILENAME)
