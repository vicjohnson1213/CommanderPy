import sys
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


class Argument(object):
    def __init__(self, raw_name, parse):
        super(Argument, self).__init__()

        if not re.match(r'^[\[\<][a-zA-Z0-9]+(?:\.\.\.)?[\]\>]$', raw_name):
            print >> sys.stderr, 'error: invalid argument description: {}'.format(raw_name)

        self.raw_name = raw_name
        self.parse = parse
        self.required = '<' in raw_name
        self.optional = '[' in raw_name
        self.variadic = '...' in raw_name

        if self.variadic:
            self.name = raw_name[1:-4]
        else:
            self.name = raw_name[1:-1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
        

class Program(object):
    def __init__(self):
        super(Program, self).__init__()
        self.possible_options = []
        self.possible_arguments = []
        self.unknown_args = []
        self.options = {}
        self.arguments = {}
        self.usage_str = ''
        self.name_str = ''
        self.description_str = ''
        self.allow_unknown = False
        self.addHelp = True

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

    def has_required_arg(self):
        return any(arg.required for arg in self.possible_arguments)

    def allow_unknown_options(self):
        self.allow_unknown = True
        return self

    def noHelp(self):
        self.addHelp = False
        return self

    def find_option(self, flag):
        for opt in self.possible_options:
            if opt.flag_match(flag):
                return opt

    def parse(self, raw_args):
        def set_variadic_argument(raw_arg, name, parsed_arg_list, possible_arg_list):
            if len(possible_arg_list) > 1:
                print >> sys.stderr, 'error: variadic arguments must be last: {}'.format(new_arg.raw_name)
                sys.exit(0)

            if parsed_arg_list[name]:
                parsed_arg_list[name].append(raw_arg)
            else:
                parsed_arg_list[name] = [raw_arg]

        def parse_arg(raw_arg, parse):
            if parse:
                try:
                    return parse(raw_arg)
                except:
                    print >> sys.stderr, 'error: could not parse argument: {}'.format(raw_arg)
                    sys.exit(1)
            else:
                return raw_arg

        raw_args = self.normalize(raw_args[1:])

        if self.addHelp:
            self.possible_options.append(Option('-h, --help', 'Display this help and usage information.', None, None))

            if '-h' in raw_args:
                self.displayHelp()
                sys.exit(0)

        last_opt = None

        while raw_args:
            raw_arg = raw_args.pop(0)

            if raw_arg[0] == '-':

                opt = self.find_option(raw_arg)

                if not opt:
                    if self.allow_unknown:
                        self.unknown_args.append(raw_arg)
                    else:
                        print >> sys.stderr, 'error: unknown option: {}'.format(raw_arg)
                        sys.exit(1)

                last_opt_fulfilled = (last_opt and
                    len(last_opt.arguments) > 0 and
                    last_opt.arguments[0].variadic and
                    self.options[last_opt.name] and
                    len(self.options[last_opt.name]) > 0)

                if last_opt and last_opt.has_required_arg() and not last_opt_fulfilled:
                    print >> sys.stderr, 'error: option missing required argument: {}'.format(last_opt.long)
                    sys.exit(1)

                if opt.isFlag:
                    self.options[opt.name] = True

                last_opt = opt

            else:

                if not last_opt or len(last_opt.arguments) == 0:
                    new_arg = self.possible_arguments[0]
                    raw_arg = parse_arg(raw_arg, new_arg.parse)


                    if new_arg.variadic:
                        set_variadic_argument(raw_arg, new_arg.name, self.arguments, self.possible_arguments)
                    else:
                        self.arguments[new_arg.name] = raw_arg
                        self.possible_arguments.pop(0)

                else:
                    raw_arg = parse_arg(raw_arg, last_opt.arguments[0].parse)

                    if last_opt.arguments[0].variadic:
                        set_variadic_argument(raw_arg, last_opt.name, self.options, last_opt.arguments)
                    else:
                        self.options[last_opt.name] = raw_arg


        last_arg = self.possible_arguments[0]
        last_arg_fulfilled = (len(self.possible_arguments) > 0 and
            last_arg.variadic and
            self.arguments[last_arg.name] and
            len(self.arguments[last_arg.name]) > 0)

        if self.has_required_arg() and not last_arg_fulfilled:
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
