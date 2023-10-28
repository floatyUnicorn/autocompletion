import json
import sys
import enum


class ParameterTypes(str, enum.Enum):
    any = "ANY"
    file = "FILE"


class ParameterTypeOptions:
    def __init__(
        self,
        parameter_type: ParameterTypes,
        optional: bool,
    ):
        self.parameter_type = parameter_type
        self.optional = optional

    def print(self):
        print(f"  - type: {self.parameter_type}\n    optional: {self.optional}\n")

    def __eq__(self, obj):
        if type(self) == type(obj):
            if self.parameter_type == obj.parameter_type and self.optional == obj.optional:
                return True
        return False


class CommandOptionBase:
    def __init__(
        self,
        name: str,
        param_min_amnt: int,
        param_max_amnt: int,
        parameter_type_options: list[ParameterTypeOptions],
    ):
        self.name = name
        self.param_min_amnt = param_min_amnt
        self.param_max_amnt = param_max_amnt
        self.parameter_type_options = parameter_type_options


class Command(CommandOptionBase):
    def __init__(
        self,
        options: list[str],
        name: str,
        param_min_amnt: int,
        param_max_amnt: int,
        parameter_type_options: list[ParameterTypeOptions],
    ):
        self.options = options
        super().__init__(
            name=name,
            param_min_amnt=param_min_amnt,
            param_max_amnt=param_max_amnt,
            parameter_type_options=parameter_type_options,
        )

    def __eq__(self, obj):
        if type(self) == type(obj):
            if len(self.options) == len(obj.options):
                for o in self.options:
                    if o not in obj.options:
                        return False
            else:
                return False

            if len(self.parameter_type_options) == len(obj.parameter_type_options):
                for p in self.parameter_type_options:
                    if p not in obj.parameter_type_options:
                        return False
            else:
                return False

            if self.name == obj.name and self.param_min_amnt == obj.param_min_amnt and self.param_max_amnt == obj.param_max_amnt:
                return True

        return False

    def print(self):
        print(
            f"\nCOMMAND: {self.name}\nminimum amount parameters: {self.param_min_amnt}\nmaximum amount parameters: {self.param_max_amnt}\n"
        )
        if len(self.parameter_type_options) > 0:
            print("parameter type options:")
            for parameter_type_option in self.parameter_type_options:
                parameter_type_option.print()
        if len(self.options) > 0:
            print("options:")
            for option in self.options:
                print(option)


class Option(CommandOptionBase):
    def __init__(
        self,
        long: str,
        global_option: bool,
        name: str,
        param_min_amnt: int,
        param_max_amnt: int,
        parameter_type_options: list[ParameterTypeOptions],
    ):
        self.long = long
        self.global_option = global_option
        super().__init__(
            name=name,
            param_min_amnt=param_min_amnt,
            param_max_amnt=param_max_amnt,
            parameter_type_options=parameter_type_options,
        )

    def __eq__(self, obj):
        if type(self) == type(obj):
            if len(self.parameter_type_options) == len(obj.parameter_type_options):
                for p in self.parameter_type_options:
                    if p not in obj.parameter_type_options:
                        return False
            else:
                return False

            if self.long == obj.long and self.global_option == obj.global_option and self.name == obj.name and self.param_min_amnt == obj.param_min_amnt and self.param_max_amnt == obj.param_max_amnt:
                return True

        return False

    def print(self):
        print(
            f"\nOPTION: {self.name} {self.long}\nminimum amount parameters: {self.param_min_amnt}\nmaximum amount parameters: {self.param_max_amnt}\n"
        )
        if len(self.parameter_type_options) > 0:
            print("parameter type options:\n")
            for parameter_type_option in self.parameter_type_options:
                parameter_type_option.print()


class AutoCompletion:
    config_path = ""

    commands: list[Command] = []
    options: list[Option] = []
    global_options: list[Option] = []

    def __init__(
        self,
        config_path,
        args,
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
            # when in command line read in args
            self.current_input = sys.argv[1:]
        else:
            # only for testing via pytest
            self.current_input = args

        if len(self.current_input) > 0:
            self.current_word = self.current_input[-1]
        else:
            self.current_word = None

        """
        the following code could be used for more complex completion rules when not just the last word should be 
        considered for completion
        
        self.last_global_option = None
        self.last_command = None

        last_global_option_command, self.after_option_command = self.get_last_command_global_option(
            current_input=self.current_input
        )

        if last_global_option_command is not None and isinstance(last_global_option_command, Command):
            self.last_command = last_global_option_command
        elif last_global_option_command is not None and isinstance(last_global_option_command, Option):
            self.last_global_option = last_global_option_command
        """

    def _get_parameter_type_options(
        self,
        parameters,
    ):
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

    def get_commands(self):
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
                            options=command_rules[command]["options"],
                            name=command,
                            param_min_amnt=command_rules[command]["parameters"][
                                "min_amnt"
                            ],
                            param_max_amnt=command_rules[command]["parameters"][
                                "max_amnt"
                            ],
                            parameter_type_options=parameter_type_options,
                        )
                    )

            return command_list

    def get_options(
        self,
        option_type,
    ):
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
                            global_option=(option_type == "global_option_rules"),
                        )
                    )

            return command_option_list


    def complete_file_path(
        self,
        current_word: str,
    ):
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
        current_word,
    ):
        """
        completes an input, that has already been started to be typed, if the command/option is already complete it will
        not be returned - instead the option or command will be returned. does not take into consideration already typed
        commands/options/parameters, so if a command gets typed before and the option would not be valid it will still
        be completed
        :param current_word: the started word
        :return: a list of possible completions (strings, last command, last global option, last option) of the current
            word and a bool if the current word is an exact match
        """
        if current_word is None:
            return [], False

        completion = []
        exact_match = False
        for command in self.commands:
            if command.name == current_word:
                exact_match = True
            if command.name.startswith(current_word):
                completion.append(command.name)

        for option in self.options:
            if option.name == current_word or option.long == current_word:
                exact_match = True
            if option.name.startswith(current_word):
                completion.append(option.name)
            if option.long.startswith(current_word):
                completion.append(option.long)

        for option in self.global_options:
            if option.name == current_word or option.long == current_word:
                exact_match = True
            if option.name.startswith(current_word):
                completion.append(option.name)
            if option.long.startswith(current_word):
                completion.append(option.long)

        completion.extend(self.complete_file_path(current_word=current_word))

        return completion, exact_match

    def get_last_command_global_option(
        self,
        current_input,
    ):
        """
        gets last command, option or global option - whichever appears later in input and all following input
        :param current_input: parameters passed by command line script, those are the entered words in order by the user
        :return: either command or option (as a tuple - COMMAND, OPTION) - max one will be not none
        """
        for word in reversed(current_input):
            command = next((command for command in self.commands if command.name == word), None)
            if command is not None:
                return command, None

            global_option = next((option for option in self.global_options if option.name == word or option.long == word), None)
            if global_option is not None:
                return None, global_option

            option = next((option for option in self.options if option.name == word or option.long == word), None)
            if option is not None:
                return None, option

        return None, None

    def complete_next(
        self,
        last_word_command,
        last_word_option,
    ):
        """
        this function could be extended to contain completion for parameters, currently will only complete the options
        for the last command and the types of parameters that could be added for the given option/command
        :param last_word_command: the last command that was contained in the user input
        :param last_word_option: the last option/global option that was contained in the user input
        only one of the parameters will get passed, as it only makes sense completing the last
        :return: a list of strings, containing all options and parameter types that could be typed after the last option
        or command
        """
        completion: list[str] = []

        if last_word_command is not None:
            completion.extend(last_word_command.options)

            for parameter_type_option in last_word_command.parameter_type_options:
                completion.append(parameter_type_option.parameter_type)

        if last_word_option is not None:
            for parameter_type_option in last_word_option.parameter_type_options:
                completion.append(parameter_type_option.parameter_type)

        return completion


if __name__ == "__main__":
    input = sys.argv[1:]
    config_path = None
    # if the first input argument is --test_autocompletion_config the second argument will be used as the path to the
    # test config to be used will probably only be used for test purposes
    if len(input) > 1 and input[0] == '--test_autocompletion_config':
        config_path = input[1]
    autocompletion = AutoCompletion(config_path=config_path, args=None)

    completion = []

    # the last given string will be completed at first with all specified commands, global options and options
    # if the command/option is already complete it will not show up in this list but instead as command or option
    # if this list is not empty, only those options will show up
    completion_main, exact_match = autocompletion.complete_current(current_word=autocompletion.current_word)
    completion.extend(completion_main)

    # TODO test this, write pytest for ittttt
    last_command, last_option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)
    print(last_command)
    print(last_option)
    # TODO this defenitely needs to return all global options/commands if both last_command/last_option are None
    # currently only works for completing current word
    completion_main.extend(autocompletion.complete_next(last_word_option=last_option, last_word_command=last_command))

    print(completion)


