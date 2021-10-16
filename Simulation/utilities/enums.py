from enum import Enum, auto, unique

@unique
class DeviceType(Enum):
    CONT = auto()
    AC = auto()
    COL_LIGHT = auto()
    DOOR_LOCK = auto()
    FAN = auto()
    LIGHT = auto()

@unique
class PowerStatus(Enum):
    ON = auto()
    OFF = auto()

@unique
class DoorLockStatus(Enum):
    ON = auto()
    OFF = auto()

@unique
class ACFanSpeed(Enum):
    LOW = auto()
    MID = auto()
    HIGH = auto()

@unique
class ACSwingState(Enum):
    ON = auto()
    OFF = auto()

@unique
class ACMode(Enum):
    DRY = auto()
    COOL = auto()
    FAN = auto()