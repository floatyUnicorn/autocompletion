import pytest

from src import AutoCompletion, Command, ParameterTypeOptions, ParameterTypes, Option


# executing tests currently in directory autoCompletion
# pytest tests/autocompletion_test.py


class TestAutocompletion:
    # -------------------------------- TEST CONFIGURATION/SETUP -------------------------------- #
    @pytest.mark.unit
    def test_init_config_path(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        assert autocompletion.config_path == "tests/test_configs/config_1.json"

    @pytest.mark.unit
    def test_init_config_path_none(self):
        autocompletion = AutoCompletion(config_path=None)

        assert autocompletion.config_path == "config.json"

    @pytest.mark.unit
    def test_get_commands(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_2.json")

        commands = autocompletion.get_commands()

        assert len(commands) == 0
        assert commands == []
        assert len(autocompletion.commands) == 0

    @pytest.mark.unit
    def test_get_options(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

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
            ),
            Option(
                name="-o_2",
                long="--option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_2.json")

        options = autocompletion.get_options(option_type="command_option_rules")

        assert len(options) == 0
        assert options == []
        assert len(autocompletion.options) == 0


    @pytest.mark.unit
    def test_get_options_no_long_for_some(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_4.json")

        options = autocompletion.get_options(option_type="command_option_rules")

        expected_options = [
            Option(
                name="-o_1",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
            Option(
                name="-o_2",
                long="--option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
            Option(
                name="-o_p_t_i_o_n_3",
                long="--the_awesome_option_3",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
            Option(
                name="-option4",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_2.json")

        global_options = autocompletion.get_options(option_type="global_option_rules")

        assert len(global_options) == 0
        assert global_options == []
        assert len(autocompletion.global_options) == 0

    @pytest.mark.unit
    def test_get_global_options_no_long_for_some(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_4.json")

        global_options = autocompletion.get_options(option_type="global_option_rules")

        expected_options = [
            Option(
                name="-go_1",
                long="--global_option_1",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
            Option(
                name="-go_2",
                long="--global_option_2",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
            Option(
                name="-og3",
                long="",
                param_min_amnt=0,
                param_max_amnt=0,
                parameter_type_options=[],
            ),
        ]

        assert len(global_options) == len(expected_options)
        assert len(autocompletion.global_options) == len(expected_options)

        for option in global_options:
            assert option in expected_options

        for option in autocompletion.global_options:
            assert option in expected_options

    # -------------------------------- TEST COMPLETION -------------------------------- #
    @pytest.mark.unit
    def test_complete_current_command_1(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="c")

        expected = [
            "c_1",
            "c_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_2(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="c_")

        expected = [
            "c_1",
            "c_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_3(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_3.json")

        completed = autocompletion.complete_current(current_word="c")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_3.json")

        completed = autocompletion.complete_current(current_word="thi")

        expected = [
            "this_is_command_4",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_command_5(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_3.json")

        completed = autocompletion.complete_current(current_word="the")

        assert len(completed) == 0

    @pytest.mark.unit
    def test_complete_current_command_6(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="a")

        assert len(completed) == 0

    @pytest.mark.unit
    def test_complete_current_command_7(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_3.json")

        completed = autocompletion.complete_current(current_word="c_")

        expected = [
            "c_2",
            "c_o_m_m_a_n_d_5",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_1(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="-")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="--")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="-o")

        expected = [
            "-o_1",
            "-o_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_4(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_1.json")

        completed = autocompletion.complete_current(current_word="--g")

        expected = [
            "--global_option_1",
            "--global_option_2",
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_5(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_4.json")

        completed = autocompletion.complete_current(current_word="-")

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
            "-og3"
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected

    @pytest.mark.unit
    def test_complete_current_option_6(self):
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_4.json")

        completed = autocompletion.complete_current(current_word="--")

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
        autocompletion = AutoCompletion(config_path="tests/test_configs/config_4.json")

        completed = autocompletion.complete_current(current_word="-o")

        expected = [
            "-o_1",
            "-o_2",
            "-o_p_t_i_o_n_3",
            "-option4",
            "-og3"
        ]

        assert len(completed) == len(expected)

        for command in completed:
            assert command in expected
