# from traceback import StackSummary
# try:
#     raise ValueError('Test error')
# except ValueError as ve:
#     print(ve)
from typing import Literal, Type
from enum import Enum, auto, unique

@unique
class PW(Enum):
    A = auto()
    B = auto()

def x(y: Literal[PW.A]) -> None:
    if type(y) == Literal[PW.A]:
        print("fine")
    if y == PW.A:
        print("A")
    else:
        print("B")

x(PW.A)