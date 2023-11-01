# autocompletion

autocompletion for the command line. for a lot of command line commands some kind of autocompletion exists, this project
should enable adding completion for commands of other self implemented projects without having to use a specifically
written shell script every time.

this is a small module that implements command line autocompletion that can be configured in a `.json` file. this project
contains the logic implemented within a python script. this script will have to be called via some a shell wrapper script 
any time the user types `tab` or any other key that should be used for completion for the command to be completed. this
shell wrapper is currently not contained in this project.

## configuration

example (also used for some test cases):
```angular2html
{
  "default": "FILE",
  "command_rules": {
    "c_1": {
      "parameters": {
        "min_amnt": 1,
        "max_amnt": 3,
        "type_options": [
          {
            "type": "FILE",
            "optional": true
          },
          {
            "type": "ANY",
            "optional": true
          }
        ]
      },
      "options": ["-o_1"]
    },
    "c_2": {
      "parameters": {
        "min_amnt": 0,
        "max_amnt": 0,
        "type_options": []
      },
      "options": ["-o_1", "-o_2"]
    }
  },
  "command_option_rules": {
    "-o_1": {
      "long": "--option_1",
      "parameters": {
        "min_amnt": 0,
        "max_amnt": 1,
        "type_options": [
          {
            "type": "ANY",
            "optional": true
          }
        ]
      }
    },
    "-o_2": {
      "long": "--option_2",
      "parameters": {
        "min_amnt": 0,
        "max_amnt": 0,
        "type_options": []
      }
    }
  },
  "global_option_rules": {
    "-go_1": {
      "long": "--global_option_1",
      "parameters": {
        "min_amnt": 1,
        "max_amnt": 1,
        "type_options": [
          {
            "type": "FILE",
            "optional": false
          }
        ]
      }
    },
    "-go_2": {
      "long": "--global_option_2",
      "parameters": {
        "min_amnt": 0,
        "max_amnt": 1,
        "type_options": [
          {
            "type": "FILE",
            "optional": true
          }
        ]
      }
    }
  }
}
```
### default

the default can have two values - `ANY` or `FILE`. this field describes which is the default mode of completion, meaning
the completion will default to it.

setting the default to `ANY` will result to no completion being done if the rules do not allow any other kind of
completion as this type does not describe a completable value. could be a string, an int,...

setting the default to `FILE` will automatically complete file paths the way the operating system would complete file
paths.

### structure of command an option rules

the structure of specifying commands and options is very similar and contains mostly the same kind of variables. these
variables are described here.

#### parameters

##### min_amnt and max_amnt

##### type_options

#### options

this can only be specified for commands.

#### long

this can only be specified for options.

### command_rules

### command_option_rules

### global_option_rules

## running tests

from the base directory of the project simply run
`pytest tests/autocompletion_test.py` to execute unit tests

