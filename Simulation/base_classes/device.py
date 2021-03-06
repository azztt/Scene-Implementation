from __future__ import annotations
from enum import Enum
from types import FunctionType
from typing import Any, Dict, Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from .room import Room
from utilities import PowerStatus
from .entity import Entity

class Device(Entity):
    def __init__(self, name: str, id: str, type: Literal = None) -> None:
        super().__init__(name, id)
        self.power_status = PowerStatus.OFF
        self.room: Room = None
        self.type: Literal = type
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        print("{}Device {} in Room {}: {}".format(
            prefix, self.get_name(), 
            self.room.get_name(), errmsg
        ))
    
    def power_on(self) -> str:
        """
        Attempts to change the device power to ON.\n
        Returns None if the status was changed successfully,\n
        else returns error message,
        """
        try:
            if not self.room:
                errmsg = "Device not in any room. First add this device to a room."
                return errmsg
            self.power_status = PowerStatus.ON
        except RuntimeError as err:
            errmsg = "Could not power on the device"
            self.error(err)
            return errmsg
        else:
            return None
    
    def power_off(self) -> str:
        """
        Attempts to change the device power to OFF.\n
        Returns True with empty error if the status was changed successfully,\n
        else returns False with the error message,
        """
        try:
            self.power_status = PowerStatus.OFF
        except RuntimeError as err:
            errmsg = "Could not power off the device"
            self.error(err)
            return errmsg
        else:
            return None
    
    def place_in_room(self, room: Room) -> str:
        """
        Places this device in the room `room`.\n
        One device instance can be placed in ONLY one room.\n
        Returns None on success else an error message
        """
        try:
            self.room = room
        except RuntimeError as err:
            errmsg = "Could not place in room"
            self.error(err)
            return errmsg
    
    def remove_from_room(self) -> str:
        """
        Removes this device from the current room.\n
        The device is powered off before removing.\n
        Returns `None` on success else an error message.
        """
        try:
            err = self.power_off()
            if err:
                raise RuntimeError(err)
            self.room = None
        except RuntimeError as err:
            errmsg = "Could not remove from room"
            self.error(err)
            return errmsg
        else:
            return None

    def get_power_status(self) -> Literal:
        """
        Returns the power status (ON or OFF) of the device.
        """
        return self.power_status
    
    def get_room(self) -> Room:
        """
        Returns the room object in which this device is present.
        """
        return self.room
    
    def get_device_type(self) -> Literal:
        """
        Returns the type of this device
        """
        return self.type
    
    def get_status_string(self) -> Dict[str, Any]:
        """
        Returns the status of all attributes of the device\n
        as a dictionary with the attributes as key strings.
        """
        pass