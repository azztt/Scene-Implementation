from typing import Any, Dict, OrderedDict, Tuple
from .light import Light
from utilities import DeviceType, PowerStatus
from utilities import is_color_valid

class ColorLight(Light):
    def __init__(self, name: str, id: str,
                brightness_levels: int = 5,
                color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(name, id, brightness_levels, DeviceType.COL_LIGHT)
        if is_color_valid(color):
            self.color = color
        else:
            self.color = (255, 255, 255)
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "ColorLight->"
        super().error(errmsg, prefix)
    
    def set_color(self, color: Tuple[int, int, int]) -> str:
        """
        Sets the current color to `color` if it is valid\n
        and returns None if successful. Else returns error message
        """
        try:
            if is_color_valid(color):
                self.color = color
            else:
                errmsg = "Invalid color"
                raise ValueError(errmsg)
        except ValueError as err:
            self.error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set color due to an unexpected error."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_current_color(self) -> Tuple[int, int, int]:
        """
        Returns the current color of the light
        """
        return self.color

    def get_status_string(self) -> OrderedDict[str, Any]:
        status = OrderedDict([
            # "id": self.get_id(),
            # "type": "CLIGHT",
            ("power", self.get_power_status().value),
            ("brightness", self.get_current_brightness()),
            ("color", "({},{},{})".format(
                self.color[0],
                self.color[1],
                self.color[2]
            ))
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
            colors = config_dict["color"]
            colors = colors[1:-1]
            colors = colors.split(",")
            color = (int(colors[0]), int(colors[1]), int(colors[2]))
            self.set_color(color)
        except Exception:
            return "Failed to set status"