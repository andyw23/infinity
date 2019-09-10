from importer.components import Component
from importer.options import Part
from importer.samples import Sample


class Concert(Component):
    """Creates a Concert object"""
    type = 'CONCERT'
    elements_str = "./components/concert"

    def get_elements():
        return Component.get_elements(Concert.elements_str)

    def __init__(self, concert):
        self.type = Concert.type
        self.id = concert.get("id").upper()
        self.add_parts(concert.findall("./part"))
        if self.__has_no_parts():
            print("ERROR: Concert '{0}' has no parts".format(self.id))

    def add_parts(self, parts):
        """Add parts to the choice"""
        self.parts = {}
        for part in parts:
            par = Part(part)
            self.parts[par.id] = par

    def __has_parts(self):
        return (len(self.parts) > 0)

    def __has_no_parts(self):
        return (not self.__has_parts())

    def get_events(self, partoption=None):
        res = {}
        for part in self.parts.values():
            obj = Component.get_component_by_id(part.id)
            res[len(res)] = obj.get_events(part)
        return res


"""
LOAD ALL CONCERTS
"""
Component.load_type_objects(Concert)