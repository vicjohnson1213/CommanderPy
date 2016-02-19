from Commander import Program
import sys

program = (Program()
    .description('Some description for this program')
    .usage('python tester.py [options] <first> <second...>')
    .argument('<argument>')
    .option('-t, --thing <thingarg>',
        description='Some description for waht this option does')
    .option('--optional [optionalarg]', parse=(lambda s: s.lower()))
    .option('-f, --force', description='Force execution')
    .help(None)
    .allow_unknown_options()

    .parse(sys.argv))

print 'opts: ', program.options
print 'args: ', program.arguments
print 'unknown: ', program.unknown_arguments