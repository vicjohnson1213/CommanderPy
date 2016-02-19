# Commander Py

> Commander Py provides an efficent solution to building command line applications, inspired by Node.js' [Commander.js](https://github.com/tj/commander.js)

## API

### Program Creation

Creating a new program requires importing `Program` from `Commander` and creating a new instance of it.

*Example:*

```python
from Commander import Program

program = Program()

# Program now provides an API to add options and arguments
```

### Program Information

Information about the program can be given and will be shown by default when the user uses the `-h` flag.  The following options are available:

| Function                                  | What it does                               |
| ----------------------------------------- | ------------------------------------------ |
| `program.usage('usage')`                  | Shows the preferred usage of the program.  |
| `program.description('some description')` | Shows a description of the program.        |

### Adding Arguments

Adding expected arguments is done using the `argument` function of a program.  Arguments enclosed in angle brackets are required, while any enclosed in square brackets are optional.  The `argument` function also provides the option to add a parse function to execute with the argument received or a default value for the argument.

The values of parsed arguments are available to you via `program.arguments`, which is a dictionary with the snake-cased argument name as the key.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .argument('<argument1>')
    .argument('[argument2]', default='default value')
    .parse(sys.argv))

print program.arguments 

```

The output of this program for various command line arguments is as follows:

| Command                          | Output                                                     |
| -------------------------------- | ---------------------------------------------------------- |
| `python program.py`              | `error: missing required argument`                         |
| `python program.py first`        | `{'argument1': 'first', 'argument2': 'default value'}`     |
| `python program.py first second` | `{'argument1': 'first', 'argument2': 'second'}`            |

### Adding Options

Options can be added to the program via the `option` function of a program.  Options can have a short name (a hyphen followed by a single character), a long name (two hyphens followed by any combinations of letters, numbers, underscores, and hyphens), and expected arguments (required or optional).

The arguments passed to an option will be available through `program.options['option_name']`, which is a dictionary with the snake-cased argument name as the key.  Option arguments also accept default values and parse functions.

If an option has no arguments, it is considered a flag and will have a value of `True` if that flag is present and `False` otherwise.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .option('-r, --regular', description='A description of the option')
    .option('-t, --thing <argument>')
    .option('--optional [optionalArg]')
    .option('-d, --default [defaultArg]', default='some value')
    .parse(sys.argv))

print 'result:', program.options
```

The ouput of this program for various command line arguments is as follows:

| Command                        | Output                                                    |
| ------------------------------ | --------------------------------------------------------- |
| `python program.py -o`         | `result: {'regular': True`}                               |
| `python program.py -t`         | `error: error: option missing required argument: --thing` |
| `python program.py -t value`   | `result: {'thing': { 'argument': 'value' }}`              |
| `python program.py --optional` | `result: {'optional': { 'optionalArg': 'value' }}`        |
| `python program.py -d`         | `result: {'default': { 'defaultArg': 'some value' }}`     |

*Note:* Some key/value pairs have been omitted from the output, only relevant information is shown in the output.

### Argument Parsing

A program's `argument` and `option` functions accept a parse function that will be executed with any of the command line arguments associated with that specified argument or option.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .argument('[number]', parse=float)
    .option('-p, --parsed <parsedArg>', parse=(lambda s: s.lower()))
    .parse(sys.argv))

print 'result:', program.arguments['number'] * 10
print 'result:', program.options['parsed']['parsedArg']
```

The ouput of this program for various command line arguments is as follows:

| Command                         | Output           |
| ------------------------------- | ---------------- |
| `python program.py 1.5`         | `result: 15.0`   |
| `python program.py 10`          | `result: 100.0`  |
| `python program.py -p STRING`   | `result: string` |

### Handling Unexpected/Unknown Options

A program offers a function to allow unknown options, handily called `allow_unknown_options`.  Calling this function will prevent a program from printing an error and exiting upon parsing an unknown option.

If unknown options are allowed, they will be accumulated in `program.unknown_arguments`

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .option('-p, --parsed')
    .option('-f, --force')
    .option('-o, --other')
    .allow_unknown_options()
    .parse(sys.argv))

print 'result:', program.unknown_options
```

The ouput of this program for various command line arguments is as follows:

| Command                           | Output               |
| --------------------------------- | -------------------- |
| `python program.py -pfo`          | `result: []`         |
| `python program.py -r`            | `result: ['-r']`       |
| `python program.py -pfo --random` | `result: ['--random']` |

### Customizing the Help Option

A program allows overriding the help via the `help` function.  The `help` function allows a user to specify custom flags, a custom description message, a custom function to execute, or to omit the help option alltogether.

*Example:*

```python
from Commander import Program
import sys

def my_help():
    print 'Some custom help message or perfrom some other help actions.'

# To omit the help option:
program = (Program()
    .help(omit=True)
    .parse(sys.argv))

# To change the flags:
program = (Program()
    .help(flags='-c, --custom')
    .parse(sys.argv))

# To change the description message:
program = (Program()
    .help(description='Some help description')
    .parse(sys.argv))

# To call a custom help function:
program = (Program()
    .help(display_help=my_help)
    .parse(sys.argv))
```