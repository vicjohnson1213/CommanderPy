from Commander import Program
import sys

program = (Program()
    .description('Some description for this program')
    .usage('python tester.py [options] <first> <second...>')
    .argument('<first>')
    .argument('<second...>', parse=float)
    .option('-t, --thing [requiredArg]',
        description='Some description for waht this option does',
        parse=list)

    .option('-f, --force', description='Force execution')
    .parse(sys.argv))

print 'opts: ', program.options
print 'args: ', program.arguments
