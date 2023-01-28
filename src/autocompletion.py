import json
import sys
from typing import Optional, Union, Tuple

## TODO fixme imports
# from .schemas import ParameterTypeOptions, Option, Command # pytest
from schemas import ParameterTypeOptions, Option, Command # from command line


class AutoCompletion:
    config_path = ""

    commands: list[Command] = []
    options: list[Option] = []
    global_options: list[Option] = []

    def __init__(
        self,
        config_path: Optional[str],
        args: Optional[list[str]],
    ):
        """
        initializes completion
            - sets config file that should be used
            - loads commands, global options and options from configuration file
        :param config_path:
            - if this variable is set, this configuration gets used (mainly for test purposes)
            - if this variable is not set, the configuration is set statically (for Elektra project set using KDB)
        :param args:
            this variable should only be set for testing from pytests
            - if this variable is set, the autocompletion will be done with using this list as the previously typed commands/options
            - if this variable is not set, the autocompletion will be done based on the arguements passed via command line
        """
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = "config.json"
            # TODO set using kdb

        self.commands = self.get_commands()
        self.options = self.get_options(option_type="command_option_rules")
        self.global_options = self.get_options(option_type="global_option_rules")
        if args is None:
            self.args = sys.argv[1:]
        else: # only for testing via pytest
            self.args = args

    def _get_parameter_type_options(
        self,
        parameters,
    ) -> list[ParameterTypeOptions]:
        parameter_type_options = []
        """
        private method used by get_options and get_commands
        :param parameters: part of a JSON containing the parameters for any option/command
        :return: a list of all parameters, containing the type and if the parameter is optional
        """
        for cnt, _ in enumerate(parameters["type_options"]):
            parameter_type_options.append(
                ParameterTypeOptions(
                    parameter_type=parameters["type_options"][cnt]["type"],
                    optional=parameters["type_options"][cnt]["optional"],
                )
            )

        return parameter_type_options

    def get_commands(self) -> list[Command]:
        """
        get commands form the config file
        :return: a list of all commands
        """
        with open(self.config_path) as config:
            config_json = json.loads(config.read())
            command_list = []
            if "command_rules" in config_json:
                command_rules = config_json["command_rules"]

                for command in command_rules:
                    parameter_type_options = self._get_parameter_type_options(
                        parameters=command_rules[command]["parameters"]
                    )

                    command_list.append(
                        Command(
                            name=command,
                            param_min_amnt=command_rules[command]["parameters"][
                                "min_amnt"
                            ],
                            param_max_amnt=command_rules[command]["parameters"][
                                "max_amnt"
                            ],
                            parameter_type_options=parameter_type_options,
                            options=command_rules[command]["options"],
                        )
                    )

            return command_list

    def get_options(
        self,
        option_type: str,
    ) -> list[Option]:
        """
        get options form the config file
        :param option_type:
            command_option_rules for options following a command
            global_option_rules for gloabl options
        :return: a list of all options of that option_type, no duplicates
        """
        with open(self.config_path) as config:
            config_json = json.loads(config.read())
            command_option_list = []
            if option_type in config_json:
                command_option_rules = config_json[option_type]

                for option in command_option_rules:
                    parameter_type_options = self._get_parameter_type_options(
                        parameters=command_option_rules[option]["parameters"]
                    )

                    long = ""
                    if "long" in command_option_rules[option]:
                        long = command_option_rules[option]["long"]

                    command_option_list.append(
                        Option(
                            name=option,
                            long=long,
                            param_min_amnt=command_option_rules[option]["parameters"][
                                "min_amnt"
                            ],
                            param_max_amnt=command_option_rules[option]["parameters"][
                                "max_amnt"
                            ],
                            parameter_type_options=parameter_type_options,
                        )
                    )

            return command_option_list


    def complete_file_path(
        self,
        current_word: str,
    ) -> list[str]:
        file_list = []
        """
        completes a file path
        :param current_word: 
        :return: 
        """
        # TODO
        return file_list

    def complete_current(
        self,
        current_word: str,
    ) -> list[str]:
        """
        completes an input, that has already been started to be typed
        does not take into consideration already typed commands/options/parameters currently
        :param current_word: the started word
        :return: a list of possible completions as strings
        """
        completion = []
        for command in self.commands:
            if command.name.startswith(current_word):
                completion.append(command.name)

        for option in self.options:
            if option.name.startswith(current_word):
                completion.append(option.name)
            if option.long.startswith(current_word):
                completion.append(option.long)

        for option in self.global_options:
            if option.name.startswith(current_word):
                completion.append(option.name)
            if option.long.startswith(current_word):
                completion.append(option.long)

        completion.extend(self.complete_file_path(current_word=current_word))

        return completion

    def get_last_command_global_option(
        self,
        current_input: list[str],
    ) -> Tuple[Union[Optional[Command], Optional[Option]], list[str]]:
        """
        gets last command or global option - whichever appears later in input and all following input
        :param current_input: parameters passed by command line script, those are the entered words in order by the user
        :return: either command or option or none and a list of strings
        """
        after: list[str] = []

        for word in reversed(current_input):
            command = next((command for command in self.commands if command.name == word), None)
            if command is not None:
                return command, after

            option = next((option for option in self.global_options if option.name == word or option.long == word), None)
            if option is not None:
                return option, after

            after = [word] + after

        return None, after

    def complete(
        self,
    ) -> list[str]:
        current_input = ""
        print("YAY")
        """ WTF
        split_input, last_word = self.split_current_input(input_str=current_input)
        # check if last command is complete -- is there a space in the end? if so the last word is complete
        if len(current_input) > 1 and current_input[-1] == " ":
            # check if last command needs/can take params or flags -- will be done in second step
            # check for other commands - only complete commands that have not yet been typed (wanted)
            pass
        else:
            # complete current word
            return self.complete_current(current_word=last_word)"""
        return []


if __name__ == "__main__":
    autocompletion = AutoCompletion(config_path=None, args=None)
    # when in command line read in args - remove first argument as it is the script name
    current_input = sys.argv[1:]
    if len(current_input) > 0:
        current_word = current_input[-1]
    else:
        current_word = None

    autocompletion.get_last_command_global_option(current_input=current_input)

    last_option = None
    last_command = None

    last_option_command, after_option_command = autocompletion.get_last_command_global_option(current_input=current_input)

    if last_option_command is not None and isinstance(last_option_command, Command):
        last_command = last_option_command
    elif last_option_command is not None and isinstance(last_option_command, Option):
        last_option = last_option_command

    print(last_option)
    print(last_command)
    # ok - complete current & complete next always? -- no. return 2 lists?
    # autocompletion.complete()
