from enum import Enum, unique

@unique
class DeviceType(Enum):
    CONT = "controller"
    AC = "ac"
    COL_LIGHT = "clight"
    DOOR_LOCK = "door_lock"
    FAN = "fan"
    LIGHT = "light"

@unique
class PowerStatus(Enum):
    ON = "ON"
    OFF = "OFF"

@unique
class DoorLockStatus(Enum):
    ON = "ON"
    OFF = "OFF"

@unique
class ACFanSpeed(Enum):
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"

@unique
class ACSwingState(Enum):
    ON = "ON"
    OFF = "OFF"

@unique
class ACMode(Enum):
    DRY = "DRY"
    COOL = "COOL"
    FAN = "FAN"

@unique
class OPStatus(Enum):
    SUCCESS = "ok"
    FAILED = "failed"

# Enums for specific device operations

@unique
class FanOp(Enum):
    SET_SPEED = "set_speed"

@unique
class ACOp(Enum):
    SET_TEMP = "set_temp"
    SET_FAN_SPEED = "set_fan_speed"
    SET_SWING = "set_swing"
    SET_MODE = "set_mode"

@unique
class LightOp(Enum):
    SET_BRIGHT = "set_brightness"

@unique
class CLightOp(Enum):
    SET_BRIGHT = "set_brightness"
    SET_COLOR = "set_color"

@unique
class DoorLockOp(Enum):
    SET_LOCK = "set_lock_state"

@unique
class Error(Enum):
    NO_CONT = "No controller"