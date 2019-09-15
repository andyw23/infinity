from importer.components import Component
from importer.options import Part
from importer.samples import Sample


class Concert(Component):
    """Creates a Concert object"""
    component_type = 'CONCERT'
    elements_str = "./components/concert"

    def get_elements():
        return Component.get_elements(Concert.elements_str)

    def __init__(self, concert):
        self.component_type = Concert.component_type
        self.id = concert.get("id").upper()
        self.add_parts(concert.findall("./part"))
        if self._has_no_parts():
            print("ERROR: Concert '{0}' has no parts".format(self.id))

    def add_parts(self, parts):
        """Add parts to the choice"""
        self.parts = {}
        for part in parts:
            par = Part(self, part)
            self.parts[par.id] = par

    def _has_parts(self):
        return (len(self.parts) > 0)

    def _has_no_parts(self):
        return (not self._has_parts())

    def get_events(self, time_offset, variant_id):
        """
        Returns a list of events pertaining to this concert

        :param partoption: Part or Option
        :param time_offset: float
        :return: list of saple dictionaries and / or other concert lists
        """
        res = []
        for part in self.parts.values():
            obj = Component.get_component_by_id(part.id)
            time_offset = Component.add_time_offset_and_partoption(time_offset, part)
            res += obj.get_events(time_offset, part.variant_id)
        return res
