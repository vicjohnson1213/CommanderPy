# Things To Do

## New Stuff

- Readme and comments
- Git style subcommands
    - `git commit [options]`

## Maintenance

- Break `Option` and `Argument` into their own files.
    - I think this could help for the git style commands.

## Bugs

- If the last option was optional and there is a required argument left and there is only one more element left in `raw_args` then give the last `raw_arg` to the argument, not the option

- Options can only have one expected argument.  This should be generalized to as many arguments as the user wants.
