"""
OPTIONS CLASS
"""
import importer.components as components


class OptionPart:
    """
    Object that contains optional attribute settings
    """
    #
    def __init__(self, owner, option_part):
        # owner is the sample that owns this variant
        self.owner = owner
        self.id = option_part.get("id").upper()
        var = option_part.get("variant", None)
        self.variant = var.upper() if isinstance(var, str) else var
        self.start = components.get_length_in_seconds(owner, option_part.get("start", None))


class Option(OptionPart):
    def __init__(self, owner, option):
        super().__init__(owner, option)


class Part(OptionPart):
    def __init__(self, owner, part):
        super().__init__(owner, part)
