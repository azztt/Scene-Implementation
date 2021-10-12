from typing import Type
from utilities import PowerStatus

class Device:
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id
        self.powerStatus = PowerStatus.OFF
    
    def power_on(self) -> str:
        """
        Attempts to change the device power to ON.\n
        Returns None if the status was changed successfully,\n
        else returns error message,
        """
        try:
            self.powerStatus = PowerStatus.ON
        except RuntimeError as err:
            errmsg = "Could not power on the device"
            print("Device {}: {}".format(self.name, errmsg))
            print(err)
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
            self.powerStatus = PowerStatus.OFF
        except RuntimeError as err:
            errmsg = "Could not power off the device"
            print("{}: {}".format(self.name, errmsg))
            print(err)
            return errmsg
        else:
            return None

    def getPowerStatus(self) -> Type[PowerStatus]:
        """
        Returns the power status (ON or OFF) of the device.
        """
        return self.powerStatus