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
| `program.help('-h, --help')`              | Overrides the default help flag. (Set to `None` to omit the help option) |

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

print(program.arguments)

```

The output of this program for various command line arguments is as follows:

| Command                          | Output                                                     |
| -------------------------------- | ---------------------------------------------------------- |
| `python program.py`              | `error: missing required argument`                         |
| `python program.py first`        | `{'argument1': 'first', 'argument2': 'default value'}`     |
| `python program.py first second` | `{'argument1': 'first', 'argument2': 'second'}`            |

### Argument Parsing

By passing a function to the program's `argument` function, command line arguments van be automatically parsed.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .argument('<number>', float)
    .parse(sys.argv))

print('result:', program.arguments['number'] * 10)
```

The ouput of this program for various command line arguments is as follows:

| Command                  | Output        |
| ------------------------ | ------------- |
| `python program.py 1.5`  | `result: 15`  |
| `python program.py 10`   | `result: 100` |

### Adding Options

Options can be added to the program via the `option` function of a program.  Options can have a short name (a hyphen followed by a single character), a long name (two hyphens followed by any combinations of letters, numbers, underscores, and hyphens), and expected arguments (required or optional).

The arguments passed to an option will be available through `program.options['option_name']`, which is a dictionary with the snake-cased argument name as the key.  Option arguments also accept default values and parse functions 

If an option has no arguments, it is considered a flag and will have a value of `True` if that flag is present and `None` otherwise.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .option('-o, --option', description='A flag option.')
    .option('-t, --thing <argument>', description='An option with an argument')
    .parse(sys.argv))

print('result:', program.options)
```

The ouput of this program for various command line arguments is as follows:

| Command                        | Output                                       |
| ------------------------------ | -------------------------------------------- |
| `python program.py -o`         | `result: {'option': True`}                   |
| `python program.py -t value`   | `result: {'thing': { 'argument': 'value' }}` |