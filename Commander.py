from Argument import Argument
from Option import Option
import sys
import re

class Program(object):
    """
    The Program class allows for the creation an management of command line
    utilities, including adding options, collecting arguments for those
    options and arguments for the command.
    """
    def __init__(self):
        super(Program, self).__init__()
        self.possible_options = []
        self.possible_arguments = []
        self.unknown_arguments = []
        self.options = {}
        self.arguments = {}
        self.usage_str = ''
        self.name_str = ''
        self.description_str = ''
        self.allow_unknown_options = False
        self.help_opt = Option('-h, --help', 'Display this help and usage information.', None, None)
        self.display_help = self.default_help

    def usage(self, usage):
        """ Sets the usage string for the program """
        self.usage_str = usage
        return self

    def description(self, desc):
        """ Sets the description string for the pregram """
        self.description_str = desc
        return self

    def option(self, flags, description=None, default=None, parse=None):
        """
        Adds an option to the program and initializes the value of the option
        to the specified default or to `None`
        """
        opt = Option(flags, description, default, parse)
        self.possible_options.append(opt)

        if len(opt.arguments) > 0:
            self.options[opt.name] = {}

            for arg in opt.arguments:
                self.options[opt.name][arg.name] = default or None
        else:
            self.options[opt.name] = False

        return self

    def argument(self, arg, default=None, parse=None):
        """
        Adds an argument to the command and initalizes the value of the argument
        to a specified default or to `None`
        """
        arg = Argument(arg, parse)
        self.possible_arguments.append(arg)
        self.arguments[arg.name] = default or None
        return self

    def has_required_arg(self):
        """ Checks whether any of the unsatisfied arguments are required """
        return any(arg.required for arg in self.possible_arguments)

    def allow_unknown_options_options(self):
        """ If called, the program will not exit on unknown options """
        self.allow_unknown_options = True
        return self

    def help(self, omit=False, flags='-h, --help', description=None, display_help=None):
        """
        Alter the behavior of the help flag.  Users can change the flags, description,
        function to execute, or omit the help option alltogether.
        """

        if not omit:
            self.help_opt = Option(flags, description, None, None)
        else:
            self.help_opt = None

        self.display_help = display_help

        return self

    def no_help(self):
        self.help_opt = None

        return self

    def default_help(self):
        """ Displays help and usage information to the user and exits """
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
        for flag, desc in zip(flags, descs):
            print '  {}'.format(flag).ljust(max_len + 5) + (desc if desc else '')
            
        print

    def parse(self, raw_args):
        """
        Given a list of options and arguments, iterate through them and parse each
        one, adding it to the program for the user to use.
        """

        def set_variadic_argument(raw_arg, name, parsed_arg_list, possible_arg_list):
            """
            Sets one value to a variadic argument, checking that the variadic
            argument is in a valid location
            """
            if len(possible_arg_list) > 1:
                print >> sys.stderr, 'error: variadic arguments must be last: {}'.format(new_arg.raw_name)
                sys.exit(1)

            if parsed_arg_list[name]:
                parsed_arg_list[name].append(raw_arg)
            else:
                parsed_arg_list[name] = [raw_arg]

        def parse_arg(raw_arg, parse):
            """ Simply parses an argument if the parse funciton is proveded """
            if parse:
                try:
                    return parse(raw_arg)
                except:
                    print >> sys.stderr, 'error: could not parse argument: {}'.format(raw_arg)
                    sys.exit(1)
            else:
                return raw_arg

        def find_option(flag):
            """ Given a flag, search for the option with that name and return it """
            for opt in self.possible_options:
                if opt.flag_match(flag):
                    return opt

        # Remove the command name from the ags list
        raw_args = self.normalize(raw_args[1:])

        if self.help_opt:
            self.possible_options.append(self.help_opt)

            if self.help_opt.short in raw_args or self.help_opt.long in raw_args:
                self.display_help()
                sys.exit(0)

        # Keep track of the previous option to properly assign names to arguments
        last_opt = None

        while raw_args:
            raw_arg = raw_args.pop(0)

            # If the argument starts with a hyphen, then it is an option
            if raw_arg[0] == '-':

                opt = find_option(raw_arg)

                # If the user didn't specify this option, then either error or
                # add it to a list of unknown options
                if not opt:
                    if self.allow_unknown_options:
                        self.unknown_arguments.append(raw_arg)
                        continue
                    else:
                        print >> sys.stderr, 'error: unknown option: {}'.format(raw_arg)
                        sys.exit(1)

                # Checks whether the last option was variadic, if it was and was
                # required, then it should have at least one argument.  If it has
                # no arguments, then error
                last_opt_fulfilled = (last_opt and
                    len(last_opt.arguments) > 0 and
                    last_opt.arguments[0].variadic and
                    self.options[last_opt.name] and
                    len(self.options[last_opt.name][last_opt.arguments[0].name]) > 0)

                if last_opt and last_opt.has_required_arg() and not last_opt_fulfilled:
                    print >> sys.stderr, 'error: option missing required argument: {}'.format(last_opt.long)
                    sys.exit(1)

                if opt.isFlag:
                    self.options[opt.name] = True

                last_opt = opt

            else:
                # If execution gets to here, then the argument is a plain argument

                # If there were no options before this or the previous option has
                # satisfied all of its arguments, then parse this as a regular argument.
                # If there was a prior option, parse the argument and add it to
                # that option
                if not last_opt or len(last_opt.arguments) == 0:
                    new_arg = self.possible_arguments[0]
                    raw_arg = parse_arg(raw_arg, new_arg.parse)

                    # If the argument is variadic, add it to the list for that
                    # argument and move to the next argument. If it is not
                    # variadic, then add it to the program and remove that arg
                    # from the list of expected arguments
                    if new_arg.variadic:
                        set_variadic_argument(raw_arg, new_arg.name, self.arguments, self.possible_arguments)
                    else:
                        self.arguments[new_arg.name] = raw_arg
                        self.possible_arguments.pop(0)

                else:
                    raw_arg = parse_arg(raw_arg, last_opt.arguments[0].parse)

                    # Check for a variadic argument to the option and parse accordingly
                    if last_opt.arguments[0].variadic:
                        set_variadic_argument(raw_arg, last_opt.arguments[0].name, self.options[last_opt.name], last_opt.arguments)
                    else:
                        self.options[last_opt.name][last_opt.arguments[0].name] = raw_arg
                        last_opt.arguments.pop(0)

        # Checks if the last argument was variadic, if it was then check if its
        # arguments were fulfilled
        if len(self.possible_arguments) > 0:
            last_arg = self.possible_arguments[0]
            last_arg_fulfilled = (len(self.possible_arguments) > 0 and
                last_arg.variadic and
                self.arguments[last_arg.name] and
                len(self.arguments[last_arg.name]) > 0)

            # If the last argument was variadic and was fulfilled, then remove it.
            if last_arg_fulfilled:
                self.possible_arguments.pop(0)

        # If the program still expects any required arguments, error
        if self.has_required_arg():
            print >> sys.stderr, 'error: missing required argument'
            sys.exit(1)

        return self

    def normalize(self, raw_args):
        """
        Go through all options and normalize them. Move combined short options
        to individual ones (`-abc` -> `-a -b -c`) and split long options with
        equals (`-option=value` -> `-option value`)
        """
        new_args = []

        while raw_args:
            arg = raw_args.pop(0)

            if arg[:2] == '--':
                new_args += arg.split('=')

            elif arg[0] == '-':
                # Remove the first `-` and add a new `-` to each letter
                new_args += map(lambda s: '-' + s, list(arg[1:]))

            else:
                # If execution reaches this point, the arg is just a plain argument
                new_args.append(arg)

        return new_args
