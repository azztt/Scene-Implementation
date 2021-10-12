from enum import Enum, auto, unique

@unique
class PowerStatus(Enum):
    ON = auto()
    OFF = auto()