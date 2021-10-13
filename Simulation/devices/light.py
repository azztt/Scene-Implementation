from typing import Tuple
from Simulation.utilities.utils import PowerStatus
from base_classes import Device

class Light(Device):
    def __init__(self, name: str, id: int, brightness_levels: int = 5) -> None:
        super().__init__(name, id)
        self.brightness_levels = brightness_levels
        self.current_brightness = 0
    
    def __error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Light->"
        super().__error(errmsg, prefix)
    
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
            self.__error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set brightness level"
            self.__error(err)
            return errmsg
        else:
            return None