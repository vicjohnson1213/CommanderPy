from Commander import Program
import sys

program = (Program()
    .description('Some description for this program')
    .usage('python tester.py [options] <argument>')
    .argument('<first>', parse=float)

    .option('-t, --thing <requiredArg>',
        description='Some description for waht this option does')

    .option('-o, --other [optionalArg]',
        description='Some description for waht this option does',
        default='default value')
    
    .option('-f, --force', description='Force execution')
    .parse(sys.argv))

print 'opts: ', program.options
print 'args: ', program.arguments
