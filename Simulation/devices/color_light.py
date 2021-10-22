from typing import Any, Dict, Tuple
from .light import Light
from utilities import DeviceType
from utilities import is_color_valid

class ColorLight(Light):
    def __init__(self, name: str, id: str,
                color: Tuple[int, int, int] = (255, 255, 255),
                brightness_levels: int = 5) -> None:
        super().__init__(name, id, brightness_levels, DeviceType.COL_LIGHT)
        if is_color_valid(color):
            self.__color = color
        else:
            self.__color = (255, 255, 255)
    
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
                self.__color = color
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
        return self.__color

    def get_status_string(self) -> Dict[str, Any]:
        status = {
            "id": self.get_id(),
            "brightness": self.get_current_brightness(),
            "color": "({},{},{})".format(
                self.__color[0],
                self.__color[1],
                self.__color[2]
            )
        }
        return status