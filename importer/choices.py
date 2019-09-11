import random
import logging

from importer.components import Component
from importer.samples import Sample
from importer.options import Option

class Choice(Component):
    """Creates a Choice object"""
    component_type = 'CHOICE'
    elements_str = "./components/choose"

    def get_elements():
        return Component.get_elements(Choice.elements_str)

    def __init__(self, choice):
        self.component_type = Choice.component_type
        self.id = choice.get("id").upper()
        self.add_options(choice.findall("./part"))
        if self.__has_no_options():
            logging.error("Choice '{0}' has no parts".format(self.id))

    def add_options(self, parts):
        """Add parts to the choice"""
        self.options = {}
        for part in parts:
            par = Option(self, part)
            self.options[par.id] = par

    def __has_options(self):
        return (len(self.options) > 0)

    def __has_no_options(self):
        return (not self.__has_options())

    def __get_random_option(self):
        return random.choice(list(self.options.values()))

    def __get_option_object_by_id(self, option_id):
        return Component.get_component_by_id(option_id)

    def get_events(self, partoption=None):
        """
        :param partoption: Option
        :return: List
        """
        # choose at random between the available options
        option = self.__get_random_option()
        # get the component object indicated by the chosen option
        obj = self.__get_option_object_by_id(option.id)
        # play the object, passing on the option
        return obj.get_events(option)


"""
LOAD ALL CHOICES
"""
Component.load_type_objects(Choice)
