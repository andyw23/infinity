from importer.components import *

import xml.etree.ElementTree as ET


class Sample(Component):
    """Creates a Sample object"""
    component_type = 'SAMPLE'
    elements_str = "./components/sample"

    def get_elements():
        return Component.get_elements(Sample.elements_str)

    def __init__(self, sample):
        self.component_type = Sample.component_type
        self.id = sample.get("id").upper()
        self.file = sample.get("file")
        self.length = get_length_in_seconds(sample.get("length"))
        self.add_variants(sample.findall("./variant"))

    def add_variants(self, vars):
        "adds variants"
        self.variants = {}
        for var in vars:
            var = Variant(var)
            if var.id in self.variants.keys():
                print("ERROR: SAMPLE '{0}', VARIANT '{1}' has a duplicate id".format(self.id, var.id))
            self.variants[var.id] = var

    def get_variant_by_id(self, variant_id):
        if (variant_id == None):
            return None
        elif not variant_id in self.variants.keys():
            print("ERROR: VARIANT '{0}' NOT FOUND IN SAMPLE: '{1}'".format(variant_id, self.id))
            print("VARIANTS: ", self.variants)
        else:
            return self.variants[variant_id]

    def get_events(self, partoption=None):
        variant = None if (partoption == None) else self.get_variant_by_id(partoption.variant)
        return {'SAMPLE_ID': self.id, 'SAMPLE': self, 'VARIANT': variant}


class Variant:
    """
    Creates a Sample Variant object
    """

    def __init__(self, variant):
        self.id = variant.get("id").upper()
        self.loopcount = variant.get("loopcount", None)
        self.looplength = variant.get("looplength", None)
        self.loopStartTime = get_length_in_seconds(self, variant.get("loopStartTime", None))
        self.loopEndTime = get_length_in_seconds(self, variant.get("loopEndTime", None))
        self.add_dynamics(variant.findall("./dynamics"))

    def add_dynamics(self, dynamics):
        self.dynamics = {}
        for instruction in dynamics:
            inst = Instruction(instruction)


class Instruction:
    def __init__(self, instruction):
        self.time = instruction.get("time")
        self.level = instruction.get("level")


"""
LOAD ALL  SAMPLES
"""
Component.load_type_objects(Sample)