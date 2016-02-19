# Things To Do

## New Stuff

- Readme and comments
- Git style subcommands
    - `git commit [options]`
- Unit tests
- add option to pass a function to help to execute on a help flag instead of the default

## Maintenance

## Bugs

- If the last option was optional and there is a required argument left and there is only one more element left in `raw_args` then give the last `raw_arg` to the argument, not the option

### Fixed Buges and Completed Maintenance

- Options can only have one expected argument.  This should be generalized to as many arguments as the user wants.
- There is a lot of duplicated code around variadic arguments for options and regular options.. Find a way to consolidate that.
- Break `Option` and `Argument` into their own files.
    - I think this could help for the git style commands.
- Add a help function so the user can set their own help flag.
- If there are two arguments for an option only the last one is saved.  this should be fixed by giving each option an array of `Argument`s.  This would require an option to return the option not the program so there would need to be a better way to terminate an option..