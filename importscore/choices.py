# ##############################################################################
#  Infinity. Copyright (c) 2019 Oliver Wyman Digital and Andy Wilson. This     #
#  file is subject to the terms and conditions defined in the file 'LICENSE',  #
#  which is part of this source code package.                                  #
# ##############################################################################

import random
import logging

from importscore.components import Component
from importscore.samples import Sample
from importscore.options import Option

class Choice(Component):
    # Creates a Choice object
    # Sample, Score, Choice and Concert are the basic components of a score
    component_type = 'CHOICE'
    elements_str = "./components/choose"

    def __init__(self, choice):
        self.component_type = Choice.component_type
        self.id = choice.get("id").upper()
        self.add_options(choice.findall("./part"))
        if self._has_no_options():
            logging.error("Choice '{0}' has no parts".format(self.id))

    def add_options(self, parts):
        """Add parts to the choice"""
        self.options = {}
        for part in parts:
            par = Option(self, part)
            self.options[par.id] = par

    def _has_options(self):
        return (len(self.options) > 0)

    def _has_no_options(self):
        return (not self._has_options())

    def _get_random_option(self):
        return random.choice(list(self.options.values()))

    def _get_option_object_by_id(self, option_id):
        return Component.get_component_by_id(option_id)

    def get_sample_components(self, time_offset, variant_id, depth):
        """
        :param partoption: Part or Option
        :param time_offset: float
        :param depth: -> int : How deep down we are into the component tree
        :return: List
        """
        # choose at random between the available options
        option = self._get_random_option()
        # get the component object indicated by the chosen option
        obj = self._get_option_object_by_id(option.id)
        # play the object, passing on the option.variant_id
        return [] + obj.get_sample_components(time_offset, option.variant_id, ++depth)

    """
    CLASS METHODS
    """
    def get_elements():
        return Component.get_elements(Choice.elements_str)

