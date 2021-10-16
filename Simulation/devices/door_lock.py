from typing import Literal
from base_classes import Device, Room
from utilities import DoorLockStatus, DeviceType

class DoorLock(Device):
    def __init__(self, name: str, id: str, room: Room) -> None:
        super().__init__(name, id, DeviceType.DOOR_LOCK)
        self.__lock_state = DoorLockStatus.OFF
    
    def __error(self, errmsg: str, prefix: str = "") -> None:
        prefix = prefix + "DoorLock->"
        super().__error(errmsg, prefix=prefix)
    
    def set_lock_state(self, lock_state: Literal[DoorLockStatus.OFF]) -> str:
        """
        Sets the door lock status to `lock_state`.\n
        Return `None` on success, else returns the error message.
        """
        try:
            self.__lock_state = lock_state
        except RuntimeError as err:
            errmsg = "Could not set lock status."
            self.__error(err)
            return errmsg
        else:
            return None
    
    def get_lock_state(self) -> Literal[DoorLockStatus.OFF]:
        return self.__lock_state
