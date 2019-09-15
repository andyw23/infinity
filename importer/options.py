"""
OPTIONS CLASS
"""
import importer.components as components
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
        If the start string contains '*', the Option.random is set to True
        Later, when interpreting the sampel data, the interpreter can ask for a randomised 
        """
        randomise_char = "*"
        start_str = option_part.get("start", None)
        self.random = (isinstance(start_str, str) and (start_str.find(randomise_char) > -1))
        if self.random:
            start_str = start_str.replace(randomise_char, '')
        self.start = components.get_time_value(owner, start_str)

    def get_start_maybe_randomised(self):
        # self._start if self.random else random.random(self._start)
        if self.random:
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
