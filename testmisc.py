# import sys, os

# sys.path.append("./Simulation")

# from traceback import StackSummary
# try:
#     raise ValueError('Test error')
# except ValueError as ve:
#     print(ve)

# from typing import Literal, Type
# from enum import Enum, unique

# @unique
# class PW(Enum):
#     A = "A"
#     B = "B"

# x = PW.A

# print(x.value)

# def x(y: Literal[PW.A]) -> None:
#     if type(y) == Literal[PW.A]:
#         print("fine")
#     if y == PW.A:
#         print("A")
#     else:
#         print("B")

# x(PW.A)

# from types import FunctionType


# def B(a: int, b: int) -> int:
#     return a+b

# def A() -> FunctionType:
#     return B

# x = A()
# print(x(2,3))
# from types import FunctionType


# class X:
#     def __init__(self) -> None:
#         self.sp = 0

#     def op(self, a: int, b: int) -> int:
#         self.sp = a+b
#         return self.sp
    
#     def getop(self) -> FunctionType:
#         return self.op

# b = X()

# # com = 

# y = b.getop()

# print(y(2,3))



# color_string = "(255,255,255)"
# color_string = color_string[1:-1]
# color_codes = color_string.split(",")
# color = list(map(int, color_codes))
# color = tuple(color)
# print(color)

# import json

# s = 

# from time import sleep
# import json
# # from Simulation.devices import Fan
# import pickle

# class Fan:
#     def __init__(self, name: str, id: str, speed_levels: int):
#         self.__name = name
#         self.__id = id
#         self.__speed_levels = speed_levels
#         self.__speed = 0
    
#     def set_speed_level(self, speed: int):
#         self.__speed = speed
    
#     def get_name(self):
#         return self.__name

# fan1 = Fan(
#     name="fan 1",
#     id="1",
#     speed_levels=5
# )

# fan1.set_speed_level(3)

# fan2 = Fan(
#     name="fan 2",
#     id="2",
#     speed_levels=3
# )

# fan2.set_speed_level(2)

# objs = {
#     "fan1": [fan1],
#     "fan2": [fan2]
# }

# with open("lastStatus.log", 'wb') as file:
#     pickle.dump(objs, file)

# fan1 = None
# fan2 = None
# objs = {}

# sleep(5)

# with open("lastStatus.log", 'rb') as file:
#     objs = pickle.load(file)

# print(objs)
# print("")

# fan1 = objs.get("fan1")[0]
# fan2 = objs.get("fan2")[0]

# print("fan 1: {}".format(fan1.get_name()))
# print("fan 2: {}".format(fan2.get_name()))

z = ["x", "r"]

def m():
    global z
    z = ["a", "b", "c"]

m()
print(z)