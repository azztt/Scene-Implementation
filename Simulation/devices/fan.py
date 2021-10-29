from types import FunctionType
from typing import Any, Dict, Literal
from base_classes import Device
from utilities import PowerStatus, DeviceType
from utilities import FanOp

class Fan(Device):
    def __init__(self, name: str, id: str, speed_levels: int = 5) -> None:
        super().__init__(name, id, DeviceType.FAN)
        self.__speed_levels = speed_levels
        self.__current_speed_level = 1
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Fan->"
        super().error(errmsg, prefix)
    
    def set_speed_level(self, level: int) -> str:
        """
        Sets fan's speed level to `level` if\n
        it is within the speed levels.\n
        Returns `None` on success, else an error message.
        """
        try:
            if level <= self.__speed_levels and level >0:
                if self.get_power_status() == PowerStatus.OFF:
                    err = self.power_on()
                    if err:
                        raise RuntimeError(err)
                self.__current_speed_level = level
            else:
                errmsg = "Speed level beyond limit"
                raise ValueError(errmsg)
        except ValueError as err:
            self.error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set speed level"
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_speed_level(self) -> int:
        """
        Returns the current speed level of the fan
        """
        return self.__current_speed_level
    
    def get_status_string(self) -> Dict[str, Any]:
        status = {
            "id": self.get_id(),
            "type": "FAN",
            "speed": self.__current_speed_level
        }
        return status
    
    def get_param_string(self) -> str:
        param = "speedLevels:{}".format(self.__speed_levels)
        return param
    
    def set_from_param_string(self, status_string: str) -> str:
        config_dict: Dict[str, str] = {}
        config = status_string.split("|")
        for con in config:
            params = con.split(":")
            config_dict[params[0]] = params[1]
        try:
            self.__current_speed_level = int(config_dict["speed"])
        except Exception:
            return "Failed to set status"