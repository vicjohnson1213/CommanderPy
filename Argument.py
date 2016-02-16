import sys
import re

class Argument(object):
    """
    The Argument class represents a single argument to either the program on an
    option.
    """
    def __init__(self, raw_name, parse):
        super(Argument, self).__init__()

        # Options must start and end with square brackets or angle brackets."""
        if not re.match(r'^[\[\<][a-zA-Z0-9]+(?:\.\.\.)?[\]\>]$', raw_name):
            print >> sys.stderr, 'error: invalid argument description: {}'.format(raw_name)
            sys.exit(1)

        self.raw_name = raw_name
        self.parse = parse
        self.required = '<' in raw_name
        self.optional = '[' in raw_name
        self.variadic = '...' in raw_name

        # When naming, remove the brackets and ellipses (for variadic arguments)
        if self.variadic:
            self.name = raw_name[1:-4]
        else:
            self.name = raw_name[1:-1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)