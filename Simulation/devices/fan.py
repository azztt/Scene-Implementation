from _typeshed import Self
from base_classes import Device

class Fan(Device):
    def __init__(self, name: str, id: int, speed_levels: int = 5) -> None:
        super().__init__(name, id)
        self.speed_levels = speed_levels
    
    def set_speed_level(self, level: int) -> str:
        """
        Sets fan's speed level to `level` if\n
        it is within the speed levels.\n
        Returns `None` on success, else an error message.
        """
        try:
            if level <= self.speed_levels and level >=0:
                self.speed_levels = level
            else:
                errmsg = "Speed level beyond limit."
                raise ValueError(errmsg)
        except ValueError as err:
            print(err)
            return err
        except RuntimeError as err:
            print(err)
            print("Fan {}: Could not set speed level.", self.id)
            return err
        else:
            return None