import sys
import re

class OptContainer(object):
    """docstring for OptContainer"""
    pass   

class Option(object):
    """docstring for Option"""
    def __init__(self, flags, desc, parse):
        super(Option, self).__init__()
        self.flags = flags
        self.description = desc
        self.required = '<' in flags
        self.optional = '[' in flags
        self.variadic = '...' in flags
        self.isflag = not self.required and not self.optional and not self.variadic
        self.parse = parse

        match = re.match(r'(?:(-[a-zA-Z])[,\| ]+)?(--([^\s]+))', flags)

        if match:
            self.short = match.group(1)
            self.long = match.group(2)

            name = match.group(3)
            lowers = map(lambda s: s.lower(), re.split(r'\W+', name))
            self.name = '_'.join(lowers)

    def __str__(self):
        return str((self.short, self.long, self.name))

    def __repr__(self):
        return str((self.short, self.long, self.name))

    def isOption(self, opt):
        return opt == self.short or opt == self.long     


class Program(object):
    """docstring for Program"""
    def __init__(self):
        super(Program, self).__init__()
        self.args = []
        self.options = OptContainer()
        self.usage_str = ''
        self.allowUnknown = False


    def option(self, flags, description='', parse=None):
        opt = Option(flags, description, parse)
        self.args.append(opt)
        setattr(self.options, opt.name, None)

        return self


    def usage(self, usage):
        self.usage_str = usage
        return self


    def description(self, desc):
        self.desc = desc
        return self

    def allowUnknownOptions(self):
        self.allowUnknown = True
        return self


    def normalizeArgs(self, args):
        newArgs = []

        for arg in args:
            if arg[:2] == '--':
                parts = arg.split('=')
                newArgs += parts

            elif arg[0] == '-':
                parts = list(arg[1:])
                parts = map(lambda p: '-' + p, parts)
                newArgs += parts

            else:
                newArgs.append(arg)

        return newArgs


    def optionFor(self, flag):
        for opt in self.args:
            if opt.isOption(flag):
                return opt


    def parse(self, args):
        args = self.normalizeArgs(args[1:])
        unknownOpts = []

        self.args.append(Option('-h, --help', 'Display help and usage information.', None))

        while args:
            arg = args.pop(0)
            opt = self.optionFor(arg)

            if not opt:
                if self.allowUnknown:
                    unknownOpts.append(arg)
                    continue
                else:
                    print >> sys.stderr, 'error: unexpected argument: {0}'.format(arg)
                    sys.exit(1)

            if opt.name == 'help':
                self.printHelp()
                sys.exit(0)

            if opt.required and (len(args) == 0 or args[0][0] == '-'):
                print >> sys.stderr, 'error: missing argument: {0}'.format(opt.long)
                sys.exit(1)

            if opt.variadic:
                self.parseVariadic(opt, args)
                break

            # if option is required, or option is optional and next arg is not a flag
            if opt.required or (opt.optional and len(args) > 0 and not args[0][0] == '-'):

                val = args.pop(0)

                if opt.parse:
                    val = opt.parse(val)

                setattr(self.options, opt.name, val)
                continue

            if opt.isflag:
                setattr(self.options, opt.name, True)

        return self


    def parseVariadic(self, opt, args):
        for arg in args:
            if arg[0] == '-':
                print >> sys.stderr, 'error: variadic argument must be last: {0}'.format(opt.long)
                sys.exit(1)

        setattr(self.options, opt.name, args)
        return self


    def printHelp(self):
        flags = []
        descs = []

        for opt in self.args:
            flags.append(opt.flags)
            descs.append(opt.description)

        maxLen = max(map(len, flags)) + 2

        print

        if self.usage_str:
            print '  Usage: ' + self.usage_str
            print

        if self.desc:
            print '  ' + self.desc
            print

        for row in zip(flags, descs):
            print '  ' + ''.join(word.ljust(maxLen) for word in row)

        print
