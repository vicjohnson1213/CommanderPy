from Argument import Argument
import re

class Option(object):
    def __init__(self, raw_flags, description, default, parse):
        super(Option, self).__init__()
        self.raw_flags = raw_flags
        self.description = description
        self.default = default
        self.arguments = []

        parts = re.split(r'[, |]+', raw_flags)

        for part in parts:
            if part[:2] == '--':
                self.long = part
            elif part[0] == '-':
                self.short = part
            else:
                self.arguments.append(Argument(part, parse))

        self.isFlag = len(self.arguments) == 0

        name = re.split(r'[^a-zA-Z0-9]+', self.long[2:])
        name = map(lambda s: s.lower(), name)
        self.name = '_'.join(name)

    def flag_match(self, flag):
        return flag == self.short or flag == self.long

    def has_required_arg(self):
        return any(arg.required for arg in self.arguments)

    def __str__(self):
        return str((self.short, self.long, self.name))

    def __repr__(self):
        return str(self)