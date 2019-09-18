"""
OPTIONS CLASS
"""
import importscore.components as components
import random

class OptionPart:
    """
    Object that contains optional attribute settings
    """
    def __init__(self, owner, option_part):
        # owner is the sample that owns this variant
        self.owner = owner
        self.id = option_part.get("id").upper()
        var = option_part.get("variant", None)
        self.variant_id = var.upper() if isinstance(var, str) else var

        """
        If the start string contains '*', option.randomise is set to True
        When interpreting sample data, if option.randomise is True the object will return a random value (0 < val < option.start) when  option.get_start_maybe_randomised() is called.
        """
        randomise_char = "*"
        start_str = option_part.get("start", None)
        self.randomise = (isinstance(start_str, str) and (start_str.find(randomise_char) > -1))
        if self.randomise:
            start_str = start_str.replace(randomise_char, '')
        self.start = components.get_time_value(owner, start_str)

    def get_start_maybe_randomised(self):
        """
        if option.randomise is True the object will return a random value (0 < val < option.start) when called.
        :return: self.start
        """
        if self.randomise:
            return random.uniform(0, self.start)
        else:
            return self.start
        # return (random.uniform(0, self.start) if self.random else self.start)

class Option(OptionPart):
    def __init__(self, owner, option):
        super().__init__(owner, option)


class Part(OptionPart):
    def __init__(self, owner, part):
        super().__init__(owner, part)
