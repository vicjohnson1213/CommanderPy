from Argument import Argument
import re

class Option(object):
    """
    The Option class represents a possible option for the program
    """
    def __init__(self, raw_flags, description, default, parse):
        super(Option, self).__init__()
        self.raw_flags = raw_flags
        self.description = description
        self.default = default
        self.arguments = []
        self.short = None

        # Split the option into its short and long names, as well as any arguments
        # that it might take
        parts = re.split(r'[, |]+', raw_flags)

        # set instance variables based on the part type
        for part in parts:
            if part[:2] == '--':
                self.long = part
            elif part[0] == '-':
                self.short = part
            else:
                self.arguments.append(Argument(part, parse))

        # If there are no arguments to the option it is simply a flag
        self.isFlag = len(self.arguments) == 0

        # snake case the long name and assign that to the regular name
        name = re.split(r'[^a-zA-Z0-9]+', self.long[2:])
        name = map(lambda s: s.lower(), name)
        self.name = '_'.join(name)

    def flag_match(self, flag):
        """ Simple helper to check for a matching flag """
        return flag == self.short or flag == self.long

    def has_required_arg(self):
        """
        Returns true if the option's argument list still has any required
        arguments
        """
        return any(arg.required for arg in self.arguments)

    def __str__(self):
        return str((self.short, self.long, self.name))

    def __repr__(self):
        return str(self)