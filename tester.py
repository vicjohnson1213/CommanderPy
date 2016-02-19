from Commander import Program
import sys

program = (Program()
    .description('Some description for this program')
    .usage('python tester.py [options] <first> <second...>')
    .argument('<first>')
    .option('-t, --thing [requiredArg] [requiredArg2]',
        description='Some description for waht this option does',
        parse=list)
    .help(None)
    .allow_unknown_options()

    .option('-f, --force', description='Force execution')
    .parse(sys.argv))

print 'opts: ', program.options
print 'args: ', program.arguments
print 'unknown: ', program.unknown_arguments
