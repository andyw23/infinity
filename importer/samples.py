import logging
import random, utils, os

import importer.components as components
from importer.components import *


class Sample(Component):
    """Creates a Sample object"""
    component_type = 'SAMPLE'
    elements_str = "./components/sample"

    def __init__(self, sample):
        self.component_type = Sample.component_type
        self.id = sample.get("id").upper()
        # if self.id == 'ALTAI DOPSH':
        #     print('DOPSH')
        self.filename = sample.get("file") + '.' + utils.AUDIO_EXTENSION
        self.filepath = os.path.abspath(os.path.join(utils.AUDIO_PATH, self.filename))
        self.length = get_time_value(self, sample.get("length"))
        self.length_ms = int(self.length * 1000)
        self.add_variants(sample.findall("./variant"))

    def add_variants(self, vars):
        "adds variants"
        self.variants = {}
        for var in vars:
            var = Variant(self, var)
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
                logging.error(
                    "Sample {0} called without variant_id has multiple variants: returning random Variant".format(
                        self.id))
                return self.get_random_variant()
        elif not variant_id in self.variants.keys():
            # the requested Variant was not found. Reuturn one at random and log an error
            logging.error("Variant '{0}' not found in Sample '{1}'".format(variant_id, self.id))
            logging.info("VARIANT_IDs: ", self.variants.keys())
            return self.get_random_variant()
        else:
            # return the requested variant. Alles gut.
            return self.variants[variant_id]

    def file_exists(self):
        if not os.path.exists(self.filepath):
            logging.error("Somple {0} is missing file {1}".format(self.id, self.filename))
            return False
        elif not os.path.isfile(self.filepath):
            logging.error("Somple {0} found {1} but it is not a file".format(self.id, self.filename))
            return False
        else:
            return True


    def get_sample_components(self, time_offset, variant_id):
        """
        :param partoption: Part or Option
        :param time_offset: float
        """
        # TODO: make sure get_variant_by_id does checks, and raises an error as appropriate
        variant = self.get_variant_by_id(variant_id)
        if isinstance(variant, str):
            print("stop a moment")
        # TODO: Rounding the time offset to a limited number of places. Is that the right thing to do?
        return [{'SAMPLE': self, 'VARIANT': variant, 'TIME_OFFSET': round(time_offset, 4)}]

    """
    CLASS METHODS
    """
    def get_elements():
        return Component.get_elements(Sample.elements_str)

    # TODO: find out if any Samples have no variants. Test somewhere. Write a test that gets event data from all loaded components
    def num_samples_without_variants():
        samps = Component.get_by_type(Sample.component_type)
        no_variants = [obj for obj in samps if len(obj.variants) == 0]
        return len(no_variants)


class Variant:
    """
    Creates a Sample Variant object
    """

    def __init__(self, owner_sample, variant):
        self.owner_sample = owner_sample
        self.id = variant.get("id").upper()

        """
        Loop Start Time
        
        The start time of the loop within the sample, in mS.
        If not specified, defaults to 0 mS
        """
        self.loopstarttime = self.get_data(variant, "loopstarttime")
        self.loopstarttime = get_time_value(self, self.loopstarttime)
        if (self.loopstarttime == None): self.loopstarttime = 0

        """
        Loop End Time
        
        The end time of the loop within the sample, in mS.
        If not specified, defaults to the loop length.
        """
        self.loopendtime = self.get_data(variant, "loopendtime")
        self.loopendtime = get_time_value(self, self.loopendtime)
        if self.loopendtime == None:
            # if loopendtime isn't set, default to the length of the sample owner
            self.loopendtime = owner_sample.length_ms
        elif self.loopendtime > owner_sample.length_ms:
            # if loopendtime is greater than the length of the sample, trim it back
            self.loopendtime = owner_sample.length_ms

        """
        Loop Sample Length
        
        Length of the entire loop: loop end time - loop start time.
        """
        self.loopsamplelength = self.loopendtime - self.loopstarttime

        """
        Loop Count

        The number of times to play the looop
        """
        self.loopcount = self.get_data(variant, "loopcount")
        if self.loopcount != None: self.loopcount = int(self.loopcount)

        """
        Loop Length

        for how long to play the sample of Loop Count == 0, ie. infinite loop
        """
        # TODO: clarify the relationship between loopcount, looplength, loopstarttime, loopendtime and their various defaults
        self.looplength = self.get_data(variant, "looplength")
        self.looplength = components.get_time_value(self, self.looplength)

    def get_data(self, variant, str):
        res = variant.find(str, None)
        return res if (res == None) else res.text

    def add_dynamics(self, dynamics):
        instructions = dynamics.findall('./instruction')
        self.dynamics = {}
        for instruction in dynamics:
            inst = Instruction(self, instruction)
            self.dynamics[inst.time] = inst


class Instruction:
    def __init__(self, owner_sample, instruction):
        self.time = instruction.get("time")
        if (self.time != None): self.time = get_time_value(owner_sample, self.time)
        self.level = instruction.get("level")
        if (self.level != None): self.level = int(self.level)
