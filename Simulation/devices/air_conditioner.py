from typing import Any, Dict, Literal, Tuple
from base_classes import Device
from utilities import ACFanSpeed, ACMode, ACSwingState, DeviceType
from utilities import is_in_range

class AirConditioner(Device):
    def __init__(self, name: str, id: str,
                temp_range: Tuple[int, int]) -> None:
        super().__init__(name, id, DeviceType.AC)
        self.__temp_range = temp_range
        self.__current_temp = (temp_range[0]+temp_range[1])/2
        self.__fan_speed = ACFanSpeed.MID
        self.__swing_state = ACSwingState.OFF
        self.__mode = ACMode.COOL
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "AirConditioner->"
        super().error(errmsg, prefix=prefix)
        
    def get_current_temp(self) -> int:
        """
        Returns current set temperature of AC.
        """
        return self.__current_temp
    
    def set_current_temp(self, temp: int) -> str:
        """
        Sets current temperature of the AC to `temp`\n
        if it is in range. Returns `None` on success, else\n
        returns an error message.
        """
        try:
            if is_in_range(temp, self.__temp_range):
                self.__current_temp = temp
            else:
                errmsg = "Temperature out of range."
                raise ValueError(errmsg)
        except ValueError as err:
            self.error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set temperature."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_fan_speed(self) -> Literal:
        """
        Returns current fan speed of AC.
        """
        return self.__fan_speed
    
    def set_fan_speed(self, fan_speed: Literal) -> str:
        """
        Sets current fan speed of the AC to `fan_speed`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.__fan_speed = fan_speed
        except RuntimeError as err:
            errmsg = "Could not set fan speed."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_swing_state(self) -> Literal:
        """
        Returns current swing state of AC.
        """
        return self.__swing_state
    
    def set_swing(self, state: Literal) -> str:
        """
        Sets swing state of the AC to `state`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.__swing_state = state
        except RuntimeError as err:
            errmsg = "Could not set swing."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_mode(self) -> Literal:
        """
        Returns current mode of AC.
        """
        return self.__mode
    
    def set_mode(self, mode: Literal) -> str:
        """
        Sets mode of the AC to `mode`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.__mode = mode
        except RuntimeError as err:
            errmsg = "Could not set mode."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_status_string(self) -> Dict[str, Any]:
        status = {
            "id": self.get_id(),
            "temperature": self.__current_temp,
            "fan_speed": self.__fan_speed.value,
            "swing_state": self.__swing_state.value,
            "mode": self.__mode.value
        }
        return status