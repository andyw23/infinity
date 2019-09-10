"""
OPTIONS CLASS
"""


class OptionPart:
    """
    Object that contains optional attribute settings
    """
    #
    def __init__(self, option_part):
        self.id = option_part.get("id").upper()
        var = option_part.get("variant", None)
        self.variant = var.upper() if isinstance(var, str) else var
        self.start = option_part.get("start", None)


class Option(OptionPart):
    def __init__(self, option):
        super().__init__(option)


class Part(OptionPart):
    def __init__(self, part):
        super().__init__(part)
