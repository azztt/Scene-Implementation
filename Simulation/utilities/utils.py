from enum import Enum, auto, unique
from typing import Tuple

@unique
class PowerStatus(Enum):
    ON = auto()
    OFF = auto()

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