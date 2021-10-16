from typing import List
from devices import Fan
from base_classes import Controller
from utilities import DeviceType
import paho.mqtt.client as mqtt

class FanController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.FAN)
        self.__running = False
        self.__fans: List[Fan] = []
        self.__client: mqtt.Client = None
    
    def __error(self, errmsg: str, fan: Fan = None) -> None:
        """
        Prints/logs error message
        """
        if fan:
            print("FanController for fan {} in Room {}: {}".format(
                fan.get_name(), 
                fan.get_room().get_name(), errmsg
            ))
        else:
            print("FanController: {}".format(errmsg))
    
    def add_fan(self, fan: Fan) -> str:
        """
        Adds the fan `fan` to the list fans\n
        controlled by this controller.\n
        Returns `None` on success, else returns\n
        the error message.
        """
        try:
            self.__fans.append(fan)
        except RuntimeError as err:
            errmsg = "Could not add fan"
            self.__error(err, fan)
            return errmsg
        else:
            return None
    
    def add_fans(self, fans: List[Fan]) -> str:
        """
        Adds the fans `fans` to the list fans\n
        controlled by this controller.\n
        Returns `None` on success, else returns\n
        the error message.
        """
        try:
            self.__fans.extend(fans)
        except RuntimeError as err:
            errmsg = "Could not add fan"
            self.__error(err)
            return errmsg
        else:
            return None

    def start(self) -> None:
        self.__running = True

