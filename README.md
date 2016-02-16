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

### Adding Arguments

Adding expected arguments is done using the `argument` function of a program.  Arguments enclosed in angle brackets are required, while any enclosed in square brackets are optional.  The `argument` function also provides the option to add a parse function to execute with the argument received.

The values of parsed arguments are available to you via `program.arguments`, which is a dictionary with the snake-cased argument name as the key.

*Example:*

```python
from Commander import Program
import sys

program = (Program()
    .argument('<argument1>')
    .argument('[argument2]')
    .parse(sys.argv))

print(program.arguments)

```

The output of this program for various command line arguments is as follows:

| Command                          | Output                                          |
| -------------------------------- | ----------------------------------------------- |
| `python program.py`              | `error: missing required argument`              |
| `python program.py first`        | `{'argument1': 'first', 'argument2': None}`     |
| `python program.py first second` | `{'argument1': 'first', 'argument2': 'second'}` |

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
