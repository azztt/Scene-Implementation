from typing import Any, Dict, Literal, OrderedDict
from utilities import PowerStatus, DeviceType, PowerStatus
from base_classes import Device

class Light(Device):
    def __init__(self, name: str, id: str, brightness_levels: int = 5,
                type: Literal = None) -> None:
        super().__init__(name, id, type if type else DeviceType.LIGHT)
        self.brightness_levels = brightness_levels
        self.current_brightness = 0
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Light->"
        super().error(errmsg, prefix)
    
    def set_brightness(self, brightness: int) -> str:
        """
        Sets the brightness level to `brightness` if within\n
        limits. Returns None on success, else an error\n
        message.
        """
        try:
            if brightness <= self.brightness_levels and brightness >0:
                if self.get_power_status() == PowerStatus.OFF:
                    err = self.power_on()
                    if err:
                        raise RuntimeError(err)
                self.current_brightness = brightness
            else:
                errmsg = "Brightness level beyond limit."
                raise ValueError(errmsg)
        except ValueError as err:
            self.error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set brightness level"
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_current_brightness(self) -> int:
        """
        Returns the current brightness level of the light
        """
        return self.current_brightness
    
    def get_status_string(self) -> OrderedDict[str, Any]:
        status = OrderedDict([
            # "id": self.get_id(),
            # "type": "LIGHT",
            "power", self.get_power_status().value,
            "brightness", self.get_current_brightness()
        ])
        return status
    
    def get_param_string(self) -> str:
        param = "brightLevels:{}".format(self.brightness_levels)
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
            self.set_brightness(int(config_dict["brightness"]))
        except Exception:
            return "Failed to set status"