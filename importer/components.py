import xml.etree.ElementTree as ET
from importer.options import Option

class Component:
    components = {}
    # names of the different types of components
    types = []

    num_types = 0
    element_root = ET.parse('scores.xml').getroot()

    def get_by_type(type_name):
        return [comp for comp in Component.components.values() if comp.type == type_name]

    def num_by_type(type_name):
        return len(Component.get_by_type(type_name))

    def has_type(type_name):
        return (Component.num_by_type(type_name) > 0)

    def add_component(obj):
        """
        Adds an individual component to the Component class master dictionary of components.

        :return: None
        """
        if obj.id.upper() in Component.components.keys():
            print("ERROR: TYPE {0}: ID '{1}' is already used in Components".format(obj.type, obj.id.upper()))
        else:
            # component added
            Component.components[obj.id.upper()] = obj
            """
            If the type of the component is not already in the Component class's list
            of component types (Component.types), add it now.
            """
            if not (obj.type in Component.types):
                Component.types.append(obj.type)
        Component.num_types = len(Component.types)

    def get_elements(elements_str):
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
            return None

    def get_option_from_element(element):
        return Option(element)