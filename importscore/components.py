"""
component.py
Andy Wilson 2019

Contains the root class for all the components of a score, the score itself, plus choose, Sample and Concert objects.
The component class contains a master dictionary of all components within a score, indexed by their unique ID. Thus any component can call on any other component.

The class also contains utility fucntions, eg., to examine, test and interrogate the component dictionsry.
"""
import logging
import xml.etree.ElementTree as ET

from importscore.options import Option
import utils


class Component:
    """
    Component Class

    Root class for component classes such as Score, Choose, Concert and Sample
    """
    # master dictionary of all component objects
    components = {}
    # names of the different types of components
    component_types = []
    num_component_types = 0

    def load_score_xml_strip_namespace():
        """
        Reads in the score XML as a string, but uses regex to remove namespace attributes from the root tag.
        Namespaces are useful for validating the score.xml file, but ElementTree doesn't like them
        :return:
        """
        import re

        f = open(utils.SCORE_FILENAME, "r")
        src_xml = f.read()
        f.close()
        src_xml = re.sub('xmlns=".*"', '', src_xml)
        src_xml = re.sub('xmlns:xsi=".*"', '', src_xml)
        src_xml = re.sub('xsi:schemaLocation=".*"', '', src_xml)
        return src_xml

    # element_root = ET.parse('scores.xml').getroot()
    # element_root = ET.ElementTree(ET.fromstring(load_score_text()).getroot()
    score_xml_string = load_score_xml_strip_namespace()
    element_root = ET.fromstring(score_xml_string)


    def get_by_type(type_name):
        # Returns from the components dictionary a list of all objects of the requested type, where the type_name argumeent must be one of the component_types in the Component.component_types list.

        # arguments:
        # :param str type_name: name of the type"""
        if not type_name in Component.component_types:
            logging.warning("Bad Type: Components of an unknown type ('{0}') were requested".format(type_name))
            logging.warning("Types Loaded: {0}", Component.component_types)
        return [comp for comp in Component.components.values() if comp.component_type == type_name]

    def num_by_type(component_type_name):
        return len(Component.get_by_type(component_type_name))

    def has_type(component_type_name):
        return (Component.num_by_type(component_type_name) > 0)

    def add_component(obj):
        """
        Adds an individual component to the Component class master dictionary of components.
        :argument: obj - a component object (score, choose, sample, concert) to be added to the components dictionary
        :return: None
        """
        if obj.id.upper() in Component.components.keys():
            logging.warning("Duplicate ID: Type {0}: ID '{1}' is already used in Components".format(obj.component_type,
                                                                                                    obj.id.upper()))
        else:
            # component added
            Component.components[obj.id.upper()] = obj
            # logging.info("{0}: '{1}' added to dictionary".format(obj.component_type, obj.id))
            """
            If the type of the component is not already in the Component class's list
            of component types (Component.component_types), add it now.
            """
            if not (obj.component_type in Component.component_types):
                Component.component_types.append(obj.component_type)
                Component.num_component_types = len(Component.component_types)
                # logging.info("TYPE: {0} added to component_types".format(obj.component_type))

    def get_elements(elements_str):
        """
        Returnes all xml sub-elements found by searching the xml element root defined in th Component Class for the element string passed as the argument

        :argument: str: element_str: defines the search pattern for getting sub elements of the element root
        :return: obj: element root
        """
        return Component.element_root.findall(elements_str)

    def load_type_objects(class_constructor):
        """
        Passed a class constructor object (eg. Choice, Concert, Sample or Score)
        the method adds all of the relevant component objects to this class's
        master list of components.

        Called by each Class module when it is imported.

        :return: None
        """
        for elem in class_constructor.get_elements():
            obj = class_constructor(elem)
            Component.add_component(obj)

    def get_component_by_id(id):
        """
        Returns an individual component object according to the id passed.
        If the id key is not found, returns None
        :return: component object or None
        """
        if id in Component.components.keys():
            return Component.components[id]
        else:
            logging.warning("Component '{0}' not found".format(id))
            return None

    def get_option_from_element(owner, element):
        return Option(owner, element)

    def add_time_offset_and_partoption(time_offset, partoption):
        # NB. one may be expressed in seconds, the other in milliseconds
        # return (time_offset + partoption.start)
        return (time_offset + partoption.get_start_maybe_randomised())


def get_time_value(owner=None, length_str=None):
    """
    Takes a string attribute and turns it into a tiem measure
    :rtype: object
    :param length_str: a string representing a length of time
    :return: float - time in seconds, None if None is
    """
    # if None is passed (which happens when a time attribute is not set), return None
    if not length_str: return None
    res = 0.0
    # if the string containst ':', interpret the first part as minutes
    if ":" in length_str:
        # split into minutes and seconds parts
        splt = length_str.split(':')
        # add minutes to total (as seconds / * 60
        res += (60 * int(splt[0]))
        length_str = splt[1]
    # interpret the string as a float and return
    try:
        res += float(length_str)
        return res
    except ValueError:
        logging.error("Time attribute '{0}', belonging to {1}: {2}, is not a float".format(length_str, owner.component_type, owner.id))