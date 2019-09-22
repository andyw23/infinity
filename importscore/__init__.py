import logging

__all__ = ['choices','concerts','samples','scores']

from importscore import *
from importscore.components import Component
from utils import SCHEMA_FILENAME, SCORE_FILENAME

# LOAD ALL COMPONENTS
Component.load_type_objects(samples.Sample)
Component.load_type_objects(choices.Choice)
Component.load_type_objects(concerts.Concert)
Component.load_type_objects(scores.Score)
# LOG THE RESULTS
logging.info("COMPONENTS CREATED: {}".format(len(Component.components)))
logging.info("TYPES FOUND: {}".format(Component.num_component_types))
for typ in Component.component_types:
    logging.info(typ + "S LOADED: {}".format(Component.num_by_type(typ)))

def score_is_valid():
    """
    Checks whether the scores XML file validates against the correspondingly named XSD file
    :return: Boolean
    """
    import xmlschema
    schema = xmlschema.XMLSchema(SCHEMA_FILENAME)
    return schema.is_valid(SCORE_FILENAME)

