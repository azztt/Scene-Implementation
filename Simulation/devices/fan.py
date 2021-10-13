from base_classes import Device

class Fan(Device):
    def __init__(self, name: str, id: int, speed_levels: int = 5) -> None:
        super().__init__(name, id)
        self.speed_levels = speed_levels
        self.current_speed_level = 1
    
    def __error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Fan->"
        super().__error(errmsg, prefix)
    
    def set_speed_level(self, level: int) -> str:
        """
        Sets fan's speed level to `level` if\n
        it is within the speed levels.\n
        Returns `None` on success, else an error message.
        """
        try:
            if level <= self.speed_levels and level >0:
                self.current_speed_level = level
            else:
                errmsg = "Speed level beyond limit"
                raise ValueError(errmsg)
        except ValueError as err:
            self.__error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not set speed level"
            self.__error(err)
            return errmsg
        else:
            return None