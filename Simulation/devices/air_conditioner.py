from time import sleep
from typing import Any, Dict, Literal, OrderedDict, Tuple
from base_classes import Device
from utilities import ACFanSpeed, ACMode, ACSwingState, DeviceType, PowerStatus
from utilities import is_in_range

class AirConditioner(Device):
    def __init__(self, name: str, id: str,
                temp_range: Tuple[int, int]) -> None:
        super().__init__(name, id, DeviceType.AC)
        self.temp_range = temp_range
        self.current_temp = (temp_range[0]+temp_range[1])/2
        self.fan_speed = ACFanSpeed.MID
        self.swing_state = ACSwingState.OFF
        self.mode = ACMode.COOL
    
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
        return self.current_temp
    
    def set_current_temp(self, temp: int) -> str:
        """
        Sets current temperature of the AC to `temp`\n
        if it is in range. Returns `None` on success, else\n
        returns an error message.
        """
        try:
            if is_in_range(temp, self.temp_range):
                self.current_temp = temp
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
        return self.fan_speed
    
    def set_fan_speed(self, fan_speed: Literal) -> str:
        """
        Sets current fan speed of the AC to `fan_speed`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.fan_speed = fan_speed
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
        return self.swing_state
    
    def set_swing(self, state: Literal) -> str:
        """
        Sets swing state of the AC to `state`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.swing_state = state
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
        return self.mode
    
    def set_mode(self, mode: Literal) -> str:
        """
        Sets mode of the AC to `mode`.\n
        Returns `None` on success, else returns an 
        error message.
        """
        try:
            self.mode = mode
        except RuntimeError as err:
            errmsg = "Could not set mode."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_status_string(self) -> OrderedDict[str, Any]:
        status = OrderedDict([
            # "id": self.get_id(),
            # "type": "AC",
            ("power", self.get_power_status().value),
            ("temperature", self.current_temp),
            ("fanSpeed", self.fan_speed.value),
            ("swingState", self.swing_state.value),
            ("mode", self.mode.value)
        ])
        return status
    
    def get_param_string(self) -> str:
        param = "tempRange:({},{})".format(self.temp_range[0], self.temp_range[1])
        return param
    
    def set_from_param_string(self, status_string: str) -> str:
        config_dict: Dict[str, str] = {}
        config = status_string.split("|")
        for con in config:
            params = con.split(":")
            config_dict[params[0]] = params[1]
        try:
            if config_dict["power"] == PowerStatus.OFF.value:
                self.power_off()
            else:
                self.power_on()
            self.current_temp = int(config_dict["temperature"])
            fs = {
                "LOW": ACFanSpeed.LOW,
                "MID": ACFanSpeed.MID,
                "HIGH": ACFanSpeed.HIGH
            }
            self.fan_speed = fs.get(config_dict["fanSpeed"])
            ss = {
                "OFF": ACSwingState.OFF,
                "ON": ACSwingState.ON,
            }
            self.swing_state = ss.get(config_dict["swingState"])
            ms = {
                "COOL": ACMode.COOL,
                "DRY": ACMode.DRY,
                "FAN": ACMode.FAN
            }
            self.mode = ms.get(config_dict["mode"])
        except Exception:
            return "Failed to set status"