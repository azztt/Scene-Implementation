from typing import Tuple
from base_classes import Controller, Device, Room

def is_color_valid(color: Tuple[int, int, int]) -> bool:
        """
        Return `True` if the passed `color` is a valid tuple\n
        in 8 bit RGB space, else returns `False` 
        """
        try:
            (r, g, b) = color
            non_negative = (r >= 0) and (g >= 0) and (b >= 0)
            bit_limit = (r < 256) and (g < 256) and (b < 256)
        except Exception as e:
            raise RuntimeError(e)
        else:
            if non_negative and bit_limit:
                return True
            else:
                return False

def is_in_range(val: int, val_range: Tuple[int, int]) -> bool:
    """
    Checks if `value` lies in the range `range`.\n
    Return `True` is yes else returns `False`.
    """
    if val >= val_range[0] and val <= val_range[1]:
        return True
    else:
        return False

def get_mqtt_topic(controller: Controller) -> str:
    """
    Generates and returns the topic name\n
    for the `controller` using it's room
    """
    topic_levels = ["simulation", controller.get_room_id(), controller.get_id()]
    return "/".join(topic_levels)