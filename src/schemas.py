import enum
from pydantic import BaseModel


class ParameterTypes(str, enum.Enum):
    any = "ANY"
    file = "FILE"


class ParameterTypeOptions(BaseModel):
    parameter_type: ParameterTypes
    optional: bool

    def print(self):
        print(f"  - type: {self.parameter_type}\n    optional: {self.optional}\n")


class Command_Option_Base(BaseModel):
    name: str
    param_min_amnt: int
    param_max_amnt: int
    parameter_type_options: list[ParameterTypeOptions]


class Command(Command_Option_Base):
    options: list[str]

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


class Option(Command_Option_Base):
    long: str
    global_option: bool

    def print(self):
        print(
            f"\nOPTION: {self.name} {self.long}\nminimum amount parameters: {self.param_min_amnt}\nmaximum amount parameters: {self.param_max_amnt}\n"
        )
        if len(self.parameter_type_options) > 0:
            print("parameter type options:\n")
            for parameter_type_option in self.parameter_type_options:
                parameter_type_option.print()
