from Commander import Program
import sys

program = Program() \
    .usage('program [flags]') \
    .description('Some description of what this program does and such.') \
    .option('-f, --force', description='Force the operation.') \
    .option('-t, --thing [thing...]', description='Something to something with', parse=float) \
    .option('--version') \
    .allowUnknownOptions() \
    .parse(sys.argv)

print program.options.thing
print program.options.force