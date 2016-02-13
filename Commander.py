import sys
import re

class Option(object):
    """docstring for Option"""
    def __init__(self, raw_flags, description, default, parse):
        super(Option, self).__init__()
        self.raw_flags = raw_flags
        self.description = description
        self.parse = parse
        self.default = default

        self.required = '<' in raw_flags
        self.optional = '[' in raw_flags
        self.variatic = '...' in raw_flags
        self.isFlag = not self.required and not self.optional

        parts = re.split(r'[, |]+', raw_flags)

        for part in parts:
            if part[:2] == '--':
                self.long = part
            elif part[0] == '-':
                self.short = part

        name = re.split(r'[^a-zA-Z0-9]+', self.long[2:])
        name = map(lambda s: s.lower(), name)
        self.name = '_'.join(name)

    def flag_match(self, flag):
        return flag == self.short or flag == self.long

    def __str__(self):
        return str((self.short, self.long, self.name))

    def __repr__(self):
        return str(self)


class Argument(object):
    """docstring for Argument"""
    def __init__(self, raw_arg, parse):
        super(Argument, self).__init__()

        if not re.match(r'^[\[\<][a-zA-Z0-9]+[\]\>]$', raw_arg):
            print 'BAD ARGUMENT DESCRIPTION'

        self.raw_arg = raw_arg
        self.parse = parse
        self.required = '<' in raw_arg
        self.optional = '[' in raw_arg
        self.variatic = '...' in raw_arg
        self.name = raw_arg[1:-1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
        

class Program(object):
    """docstring for Program"""
    def __init__(self):
        super(Program, self).__init__()
        self.possible_options = []
        self.possible_arguments = []
        self.options = {}
        self.arguments = {}
        self.usage_str = ''
        self.name_str = ''
        self.description_str = ''

    def usage(self, usage):
        self.usage_str = usage
        return self

    def description(self, desc):
        self.description_str = desc
        return self

    def option(self, flags, description=None, default=None, parse=None):
        opt = Option(flags, description, default, parse)
        self.possible_options.append(opt)
        self.options[opt.name] = default or None
        return self

    def argument(self, arg, parse=None):
        arg = Argument(arg, parse)
        self.possible_arguments.append(arg)
        self.arguments[arg.name] = None
        return self

    def find_option(self, flag):
        for opt in self.possible_options:
            if opt.flag_match(flag):
                return opt

    def parse(self, raw_args):
        raw_args = self.normalize(raw_args[1:])
        unknown_args = []

        self.possible_options.append(Option('-h, --help', 'Display this help and usage information.', None, None))

        if '-h' in raw_args:
            self.displayHelp()
            sys.exit(0)

        last_opt = None

        while raw_args:
            arg = raw_args.pop(0)

            if arg[0] == '-':
                opt = self.find_option(arg)

                if last_opt and last_opt.variatic:
                    print >> sys.stderr, 'error: variadic option must come last: {0}'.format(last_opt.long)
                    sys.exit(1)

                if last_opt and last_opt.required:
                    print >> sys.stderr, 'error: option missing required argument: {0}'.format(last_opt.long)
                    sys.exit(1)

                if not opt:
                    unknown_args.append(arg)
                    last_opt = None
                    continue

                if opt.isFlag:
                    self.options[opt.name] = True
                    last_opt = None
                    continue

                last_opt = opt

            else:
                # TODO: if the last option was optional and there is a required
                # argument left and there is only one more element left in raw_args
                # then give the last raw_arg to the argument, not the option
                if last_opt:
                    print last_opt
                    if last_opt.parse:
                        try:
                            arg = last_opt.parse(arg)
                        except:
                            print >> sys.stderr, 'error: could not parse argument: {0}'.format(arg)
                            sys.exit(1)

                    if not last_opt.variatic:
                        self.options[last_opt.name] = arg
                        last_opt = None
                        continue
                    elif last_opt.variatic:
                        if self.options[last_opt.name]:
                            self.options[last_opt.name].append(arg)
                        else:
                            self.options[last_opt.name] = [arg]

                        continue

                next_arg = self.possible_arguments.pop(0)

                if next_arg.parse:
                    try:
                        arg = next_arg.parse(arg)
                    except:
                        print >> sys.stderr, 'error: could not parse argument: {0}'.format(arg)
                        sys.exit(1)

                self.arguments[next_arg.name] = arg

        if self.possible_arguments and self.possible_arguments[0].required:
            print >> sys.stderr, 'error: missing required argument'
            sys.exit(1)

        return self

    def normalize(self, raw_args):
        new_args = []

        while raw_args:
            arg = raw_args.pop(0)

            if arg[:2] == '--':
                parts = arg[2:].split('=')
                new_args.append('--' + parts[0])

                if len(parts) > 1:
                    new_args.append(parts[1])

            elif arg[0] == '-':
                new_args += map(lambda s: '-' + s, list(arg[1:]))

            else:
                new_args.append(arg)

        return new_args

    def displayHelp(self):
        args = self.arguments.values()

        flags = []
        descs = []

        max_len = 0

        for opt in self.possible_options:
            flags.append(opt.raw_flags)
            descs.append(opt.description)
            max_len = max(max_len, len(opt.raw_flags))

        print

        if self.usage_str:
            print 'USAGE: {}'.format(self.usage_str)
            print

        if self.description_str:
            print self.description_str
            print

        print 'OPTIONS:'
        for fs, d in zip(flags, descs):
            print '  {}'.format(fs).ljust(max_len + 5) + d
        print
