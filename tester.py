from Commander import Program
import sys

program = Program() \
    .argument('<first>', parse=float) \
    .option('-t, --thing <fuck>', description='Some description for waht this fucker does') \
    .option('-f, --force', description='Force that shit') \
    .parse(sys.argv)

print 'opts', program.options
print 'args', program.arguments
