from typing import Any, Dict, Literal
from base_classes import Device
from utilities import DoorLockStatus, DeviceType

class DoorLock(Device):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.DOOR_LOCK)
        self.__lock_state = DoorLockStatus.OFF
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        prefix = prefix + "DoorLock->"
        super().error(errmsg, prefix=prefix)
    
    def set_lock_state(self, lock_state: Literal) -> str:
        """
        Sets the door lock status to `lock_state`.\n
        Return `None` on success, else returns the error message.
        """
        try:
            self.__lock_state = lock_state
        except RuntimeError as err:
            errmsg = "Could not set lock status."
            self.error(err)
            return errmsg
        else:
            return None
    
    def get_lock_state(self) -> Literal:
        return self.__lock_state
    
    def get_status_string(self) -> Dict[str, Any]:
        status = {
            "id": self.get_id(),
            "state": self.__lock_state.value
        }
        return status
