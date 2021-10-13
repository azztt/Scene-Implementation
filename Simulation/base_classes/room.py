from typing import List
from device import Entity, Device

class Room(Entity):
    def __init__(self, name: str, id: int, devices: List[Device] = []) -> None:
        super().__init__(name, id)
        self.__devices = devices
    
    def __error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        print("{}Room {}: {}".format(prefix, self.name, errmsg))
    
    def add_device(self, device: Device) -> str:
        """
        Adds a new device to the list of devices of the room.\n
        Returns None on success, else error message.
        """
        try:
            err = device.place_in_room(self)
            if err:
                raise RuntimeError(err)
            self.__devices.append(device)
        except RuntimeError as err:
            errmsg = "Could not add device to the room"
            self.__error(err)
            return errmsg
        else:
            return None
    
    def remove_device_by_id(self, device_id: int) -> str:
        """
        Removes the device with given id from the list of devices of the room.\n
        Returns None on success, else error message.
        """
        try:
            ind = 0
            for device in self.__devices:
                if device.get_id() == device_id:
                    break
                ind += 1
            if ind == len(self.__devices):
                errmsg = "Device with id {} not found.".format(device_id)
                raise ValueError(errmsg)
            
            err = self.__devices[ind].remove_from_room()
            if err:
                raise RuntimeError(err)
            self.__devices.remove(self.__devices[ind])
        except ValueError as err:
            self.__error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not remove device '{}'".format(
                device.get_name()
            )
            self.__error(err)
            return errmsg
        else:
            return None
    
    def empty_room(self) -> str:
        """
        Removes all the devices from the room. All\n
        devices are powered off before removing.\n
        Returns None on success, else an error message.
        """
        try:
            for device in self.__devices:
                err = device.remove_from_room()
                if err:
                    raise RuntimeError(err)
            
            self.__devices = []
        except RuntimeError as err:
            errmsg = "Could not remove all devices from the room."
            self.__error(err)
            return errmsg
        else:
            return None