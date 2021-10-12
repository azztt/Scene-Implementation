from typing import List
from device import Device

class Room:
    def __init__(self, name: str, id: int, devices: List[Device] = []) -> None:
        self.name = name
        self.id = id
        self.devices = devices
    
    def add_device(self, device: Device) -> str:
        """
        Adds a new device to the list of devices of the room.\n
        Returns None on success, else error message.
        """
        try:
            self.devices.append(device)
        except RuntimeError as err:
            errmsg = "Could not add device '{}' to the room.".format(
                device.name
            )
            print("Room {}: {}".format(self.name, errmsg))
            print(err)
            return errmsg
        else:
            return None
    
    def remove_device(self, device_id: int) -> str:
        """
        Removes the device with given id from the list of devices of the room.\n
        Returns None on success, else error message.
        """
        try:
            ind = 0
            for device in self.devices:
                if device.id == device_id:
                    break
                ind += 1
            if ind == len(self.devices):
                errmsg = "Room {}: Device with id {} not found.".format(self.name, device_id)
                raise ValueError(errmsg)
            
            # power off device before removing
            er = self.devices[ind].power_off()
            if er != None:
                raise RuntimeError(er)
            self.devices.remove(self.devices[ind])
        except ValueError as err:
            print(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not remove device '{}' from the room.".format(
                device.name
            )
            print("Room {}: {}".format(self.name, errmsg))
            print(err)
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
            # power off all devices
            for device in self.devices:
                er = device.power_off()
                if er != None:
                    raise RuntimeError(er)
            
            self.devices = []
        except RuntimeError as err:
            errmsg = "Could not remove all devices from the room."
            print("Room {}: {}".format(self.name, errmsg))
            print(err)
            return errmsg
        else:
            return None