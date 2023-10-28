import pytest

from src import AutoCompletion, Command, ParameterTypeOptions, ParameterTypes, Option


# executing tests currently in directory autoCompletion
# pytest tests/autocompletion_test.py


class TestAutocompletion:
    # -------------------------------- TEST CONFIGURATION/SETUP -------------------------------- #
    @pytest.mark.unit
    def test_init_config_path(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        assert autocompletion.config_path == "tests/test_configs/config_1.json"

    @pytest.mark.unit
    def test_init_config_path_none(self):
        autocompletion = AutoCompletion(
            config_path=None,
            args=[],
        )

        assert autocompletion.config_path == "config.json"

    @pytest.mark.unit
    def test_get_commands(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        commands = autocompletion.get_commands()

        expected_commands = [
            Command(
                name="c_1",
                param_min_amnt=1,
                param_max_amnt=3,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type=ParameterTypes.file,
                        optional=True,
                    ),
                    ParameterTypeOptions(
                        parameter_type=ParameterTypes.any,
                        optional=True,
                    ),
                ],
                options=[
                    "-o_1",
                ],
            ),
            Command(
                name="c_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                options=[
                    "-o_1",
                    "-o_2",
                ],
            ),
        ]

        assert len(commands) == len(expected_commands)
        assert len(autocompletion.commands) == len(expected_commands)

        for command in commands:
            assert command in expected_commands

        for command in autocompletion.commands:
            assert command in expected_commands

    @pytest.mark.unit
    def test_get_commands_empty(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_2.json",
            args=[],
        )

        commands = autocompletion.get_commands()

        assert len(commands) == 0
        assert commands == []
        assert len(autocompletion.commands) == 0

    @pytest.mark.unit
    def test_get_options(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        options = autocompletion.get_options(option_type="command_option_rules")

        expected_options = [
            Option(
                name="-o_1",
                long="--option_1",
                param_min_amnt=0,
                param_max_amnt=1,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type=ParameterTypes.any,
                        optional=True,
                    ),
                ],
                global_option=False,
            ),
            Option(
                name="-o_2",
                long="--option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=False,
            ),
        ]

        assert len(options) == len(expected_options)
        assert len(autocompletion.options) == len(expected_options)

        for option in options:
            assert option in expected_options

        for option in autocompletion.options:
            assert option in expected_options

    @pytest.mark.unit
    def test_get_options_empty(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_2.json",
            args=[],
        )

        options = autocompletion.get_options(option_type="command_option_rules")

        assert len(options) == 0
        assert options == []
        assert len(autocompletion.options) == 0

    @pytest.mark.unit
    def test_get_options_no_long_for_some(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_4.json",
            args=[],
        )

        options = autocompletion.get_options(option_type="command_option_rules")

        expected_options = [
            Option(
                name="-o_1",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=False,
            ),
            Option(
                name="-o_2",
                long="--option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=False,
            ),
            Option(
                name="-o_p_t_i_o_n_3",
                long="--the_awesome_option_3",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=False,
            ),
            Option(
                name="-option4",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=False,
            ),
        ]

        assert len(options) == len(expected_options)
        assert len(autocompletion.options) == len(expected_options)

        for option in options:
            assert option in expected_options

        for option in autocompletion.options:
            assert option in expected_options

    @pytest.mark.unit
    def test_get_global_options(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        global_options = autocompletion.get_options(option_type="global_option_rules")

        expected_options = [
            Option(
                name="-go_1",
                long="--global_option_1",
                param_min_amnt=1,
                param_max_amnt=1,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type=ParameterTypes.file,
                        optional=False,
                    ),
                ],
                global_option=True,
            ),
            Option(
                name="-go_2",
                long="--global_option_2",
                param_min_amnt=0,
                param_max_amnt=1,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type=ParameterTypes.file,
                        optional=True,
                    ),
                ],
                global_option=True,
            ),
        ]

        assert len(global_options) == len(expected_options)
        assert len(autocompletion.global_options) == len(expected_options)

        for option in global_options:
            assert option in expected_options

        for option in autocompletion.global_options:
            assert option in expected_options

    @pytest.mark.unit
    def test_get_global_options_empty(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_2.json",
            args=[],
        )

        global_options = autocompletion.get_options(option_type="global_option_rules")

        assert len(global_options) == 0
        assert global_options == []
        assert len(autocompletion.global_options) == 0

    @pytest.mark.unit
    def test_get_global_options_no_long_for_some(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_4.json",
            args=[],
        )

        global_options = autocompletion.get_options(option_type="global_option_rules")

        expected_options = [
            Option(
                name="-go_1",
                long="--global_option_1",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=True,
            ),
            Option(
                name="-go_2",
                long="--global_option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=True,
            ),
            Option(
                name="-og3",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
                global_option=True,
            ),
        ]

        assert len(global_options) == len(expected_options)
        assert len(autocompletion.global_options) == len(expected_options)

        for option in global_options:
            assert option in expected_options

        for option in autocompletion.global_options:
            assert option in expected_options

    @pytest.mark.unit
    def test_get_command_option_list_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "c_1",
                "aaaaaaaaaaaa",
                "abc/def/g",
            ],
        )

        expected = [
            Command(
                options=["-o_1"],
                name="c_1",
                param_min_amnt=1,
                param_max_amnt=3,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type="FILE",
                        optional=True,
                    ),
                    ParameterTypeOptions(
                        parameter_type="ANY",
                        optional=True,
                    ),
                ],
            ),
        ]

        assert autocompletion.get_command_option_list(autocompletion.current_input) == expected

    @pytest.mark.unit
    def test_get_command_option_list_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "c_1",
                "aaaaaaaaaaaa",
                "abc/def/g",
                "-o_1",
                "blabla",
                "--global_option_1",
                "/blub/blub/blub",
                "-"
            ],
        )

        expected = [
            Command(
                options=["-o_1"],
                name="c_1",
                param_min_amnt=1,
                param_max_amnt=3,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type="FILE",
                        optional=True,
                    ),
                    ParameterTypeOptions(
                        parameter_type="ANY",
                        optional=True,
                    ),
                ],
            ),
            Option(
                long="--option_1",
                global_option=False,
                name="-o_1",
                param_min_amnt=0,
                param_max_amnt=1,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type="ANY",
                        optional=True,
                    ),
                ],
            ),
            Option(
                long="--global_option_1",
                global_option=True,
                name="-go_1",
                param_min_amnt=1,
                param_max_amnt=1,
                parameter_type_options=[
                    ParameterTypeOptions(
                        parameter_type="FILE",
                        optional=False,
                    ),
                ],
            ),
        ]

        assert autocompletion.get_command_option_list(autocompletion.current_input) == expected

    # -------------------------------- TEST COMPLETION -------------------------------- #
    @pytest.mark.unit
    def test_complete_current_command_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="c")[0]

        expected = [
            "c_1",
            "c_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="c_")[0]

        expected = [
            "c_1",
            "c_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_3(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_3.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="c")[0]

        expected = [
            "command_1",
            "c_2",
            "c3",
            "c_o_m_m_a_n_d_5",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_4(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_3.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="thi")[0]

        expected = [
            "this_is_command_4",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_5(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_3.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="the")[0]

        assert len(completed) == 0

    @pytest.mark.unit
    def test_complete_current_command_6(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="a")[0]

        assert len(completed) == 0

    @pytest.mark.unit
    def test_complete_current_command_7(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_3.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="c_")[0]

        expected = [
            "c_2",
            "c_o_m_m_a_n_d_5",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="-")[0]

        expected = [
            "-o_1",
            "--option_1",
            "-o_2",
            "--option_2",
            "-go_1",
            "--global_option_1",
            "-go_2",
            "--global_option_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="--")[0]

        expected = [
            "--option_1",
            "--option_2",
            "--global_option_1",
            "--global_option_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_3(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="-o")[0]

        expected = [
            "-o_1",
            "-o_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_4(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="--g")[0]

        expected = [
            "--global_option_1",
            "--global_option_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_5(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_4.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="-")[0]

        expected = [
            "-o_1",
            "-o_2",
            "--option_2",
            "-o_p_t_i_o_n_3",
            "--the_awesome_option_3",
            "-option4",
            "-go_1",
            "--global_option_1",
            "-go_2",
            "--global_option_2",
            "-og3",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_6(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_4.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="--")[0]

        expected = [
            "--option_2",
            "--the_awesome_option_3",
            "--global_option_1",
            "--global_option_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_7(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_4.json",
            args=[],
        )

        completed = autocompletion.complete_current(current_word="-o")[0]

        expected = ["-o_1", "-o_2", "-o_p_t_i_o_n_3", "-option4", "-og3"]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_next_command_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        command = [c for c in autocompletion.commands if c.name == "c_1"][0]

        expected = [
            "-o_1",
            "FILE",
            "ANY",
        ]

        completed = autocompletion.complete_next(
            last_word_command=command,
            last_word_option=None,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_complete_next_command_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        command = [c for c in autocompletion.commands if c.name == "c_2"][0]

        expected = [
            "-o_1",
            "-o_2",
        ]

        completed = autocompletion.complete_next(
            last_word_command=command,
            last_word_option=None,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_complete_next_command_3(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_3.json",
            args=[],
        )

        command = [c for c in autocompletion.commands if c.name == "c_2"][0]

        expected = []

        completed = autocompletion.complete_next(
            last_word_command=command,
            last_word_option=None,
        )

        assert len(expected) == len(completed)

    @pytest.mark.unit
    def test_complete_next_option_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        option = [o for o in autocompletion.options if o.name == "-o_1"][0]

        expected = [
            "ANY",
        ]

        completed = autocompletion.complete_next(
            last_word_command=None,
            last_word_option=option,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_complete_next_option_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        option = [o for o in autocompletion.options if o.name == "-o_2"][0]

        expected = []

        completed = autocompletion.complete_next(
            last_word_command=None,
            last_word_option=option,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_complete_next_option_3(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        global_option = [o for o in autocompletion.global_options if o.name == "-go_2"][
            0
        ]

        expected = [
            "FILE",
        ]

        completed = autocompletion.complete_next(
            last_word_command=None,
            last_word_option=global_option,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_complete_next_option_4(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        expected = [
            "c_1",
            "c_2",
            "-go_1",
            "-go_2",
        ]

        completed = autocompletion.complete_next(
            last_word_command=None,
            last_word_option=None,
        )

        assert len(expected) == len(completed)

        for c in completed:
            assert c in expected

    @pytest.mark.unit
    def test_get_last_command_global_option_1(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "aaaa",
                "bbbb",
                "cc",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option is None

    @pytest.mark.unit
    def test_get_last_command_global_option_2(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option is None

    @pytest.mark.unit
    def test_get_last_command_global_option_3(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "c_1",
                "-o_1",
                "cc",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option.name == "-o_1"

    @pytest.mark.unit
    def test_get_last_command_global_option_4(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "-go_1",
                "aaa",
                "/la/bla/blub",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option.name == "-go_1"

    @pytest.mark.unit
    def test_get_last_command_global_option_5(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "--global_option_1",
                "aaa",
                "/la/bla/blub",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option.name == "-go_1"

    @pytest.mark.unit
    def test_get_last_command_global_option_6(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "--global_option",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command is None
        assert option is None

    @pytest.mark.unit
    def test_get_last_command_global_option_7(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "c_1",
                "abc/def/ghi",
                "12345",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command.name == "c_1"
        assert option is None

    @pytest.mark.unit
    def test_get_last_command_global_option_8(self):
        autocompletion = AutoCompletion(
            config_path="tests/test_configs/config_1.json",
            args=[
                "c_1",
                "-o_",
            ],
        )

        command, option = autocompletion.get_last_command_global_option(current_input=autocompletion.current_input)

        assert command.name == "c_1"
        assert option is None
