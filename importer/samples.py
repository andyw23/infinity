import importer.components as components
from importer.components import *
import logging
import random
import xml.etree.ElementTree as ET


class Sample(Component):
    """Creates a Sample object"""
    component_type = 'SAMPLE'
    elements_str = "./components/sample"

    def get_elements():
        return Component.get_elements(Sample.elements_str)

    # TODO: find out if any Samples have no variants. Test somewhere. Write a test that gets event data from all loaded components
    def num_samples_without_variants():
        samps = Component.get_by_type(Sample.component_type)
        no_variants = [obj for obj in samps if len(obj.variants) == 0]
        return len(no_variants)

    def __init__(self, sample):
        self.component_type = Sample.component_type
        self.id = sample.get("id").upper()
        # if self.id == 'ALTAI DOPSH':
        #     print('DOPSH')
        self.file = sample.get("file")
        self.length = get_time_value(self, sample.get("length"))
        self.add_variants(sample.findall("./variant"))

    def add_variants(self, vars):
        "adds variants"
        self.variants = {}
        for var in vars:
            var = Variant(var)
            if var.id in self.variants.keys():
                logging.error("Sample '{0}', Variant '{1}' has a duplicate id".format(self.id, var.id))
            self.variants[var.id] = var

    def has_variants(self):
        return (len(self.variants) > 0)

    def get_random_variant(self):
        return random.choice(list(self.variants.values()))

    def get_variant_by_id(self, variant_id):
        # if no variant_id is specified in the call
        if (variant_id == None):
            # TODO: test this
            # if there are no Variants we have a critical error
            if not self.has_variants():
                logging.critical("Sample {0} has no Variants".format(self.id))
            elif len(self.variants) == 1:
                # Called without a variant_id, the Sample has only one Variant, so return it as the default
                return list(self.variants.values())[0]
            else:
                # Called without a variant_id, the Sample has multiple Variants, so return one at random but log an error
                logging.error("Sample {0} called without variant_id has multiple variants: returning random Variant".format(self.id))
                return self.get_random_variant()
        elif not variant_id in self.variants.keys():
            # the requested Variant was not found. Reuturn one at random and log an error
            logging.error("Variant '{0}' not found in Sample '{1}'".format(variant_id, self.id))
            logging.info("VARIANT_IDs: ", self.variants.keys())
            return self.get_random_variant()
        else:
            # return the requested variant. Alles gut.
            return self.variants[variant_id]

    def get_events(self, time_offset, variant_id):
        """
        :param partoption: Part or Option
        :param time_offset: float
        """
        # TODO: make sure get_variant_by_id does checks, and raises an error as appropriate
        variant = self.get_variant_by_id(variant_id)
        if isinstance(variant, str):
            print("stop a moment")
        return [{'SAMPLE': self, 'VARIANT': variant, 'TIME_OFFSET': time_offset}]


class Variant:
    """
    Creates a Sample Variant object
    """
    def __init__(self, variant):
        self.id = variant.get("id").upper()
        self.loopcount = self.get_data(variant, "loopcount")
        if self.loopcount != None: self.loopcount = int(self.loopcount)
        self.looplength = self.get_data(variant, "looplength")
        self.looplength = components.get_time_value(self, self.looplength)
        self.loopstarttime = self.get_data(variant, "loopstarttime")
        self.loopstarttime = get_time_value(self, self.loopstarttime)
        self.loopendtime = self.get_data(variant, "loopendtime")
        self.loopendtime = get_time_value(self, self.loopendtime)
        self.starttime = self.get_data(variant, "starttime")
        self.starttime = get_time_value(self, self.starttime)
        if (self.starttime != None): self.starttime = int(self.starttime)
        self.endtime = self.get_data(variant, "endtime")
        self.endtime = get_time_value(self, self.endtime)
        if (self.endtime != None): self.endtime = int(self.endtime)
        self.add_dynamics(variant.findall("./dynamics"))

    def get_data(self, variant, str):
        res = variant.find(str, None)
        return res if (res == None) else res.text

    def add_dynamics(self, dynamics):
        self.dynamics = {}
        for instruction in dynamics:
            inst = Instruction(instruction)

class Instruction:
    def __init__(self, instruction):
        self.time = instruction.get("time")
        if (self.time != None): self.time = int(self.time)
        self.level = instruction.get("level")
        if (self.level != None): self.level = int(self.level)
