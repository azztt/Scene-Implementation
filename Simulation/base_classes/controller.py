from __future__ import annotations
from typing import Any, Dict, List, Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from .room import Room
from .device import Device
from utilities import PowerStatus, OPStatus

class Controller(Device):
    def __init__(self, name: str, id: str, type: Literal) -> None:
        super().__init__(name, id, type)
        self.__room: Room = None
        self.__devices: List[Device] = []
    
    def error(self, errmsg: str, prefix) -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Controller->"
        print("{}Controller {} in Room {}: {}".format(
            prefix, self.name, 
            self.__room.get_name() if self.__room else "None",
            errmsg
        ))
    
    def new_device_ack(self) -> str:
        """
        Method to send an update for new device addition to the\n
        server to maintain a list of those devices on server side.\n
        Returns `None` on success, else an error message.
        """
        pass
    
    def add_device(self, device: Device) -> str:
        """
        Adds a new device to this controller's device list.\n
        Return `None` on success else and error message.
        """
        try:
            self.__devices.append(device)
        except RuntimeError as err:
            errmsg = "Could not add device to the controller"
            self.error(err)
            return errmsg
        else:
            return None

    def remove_device_by_id(self, device_id: str) -> str:
        """
        Removes the device of id `device_id` from this\n
        controller's device list after switching it off.\n
        Returns `None` on success, else an error message.
        """
        try:
            done = False
            for device in self.__devices:
                if device.get_id() == device_id:
                    err = device.remove_from_room()
                    if err:
                        raise RuntimeError(err)
                    self.__devices.remove(device)
                    done = True
                    break
            
            if not done:
                errmsg = "Device with id {} not found.".format(device_id)
                raise ValueError(errmsg)
        except RuntimeError as err:
            errmsg = "Could not remove device"
            self.error(err)
            return errmsg
        else:
            return None
        

    def add_to_room(self, room: Room) -> str:
        """
        Adds controller to `room`\n
        Returns `None` on success else returns an\n
        error message.
        """
        try:
            self.__room = room
        except RuntimeError as err:
            errmsg = "Could not add controller to room"
            self.error(err)
            return errmsg
        else:
            return None
    
    def remove_from_room(self) -> str:
        """
        Removes this controller from the current room.\n
        The devices are powered off before removing.\n
        Returns `None` on success else an error message.
        """
        try:
            err = self.stop()
            if err:
                raise RuntimeError(err)
            for device in self.__devices:
                err = device.remove_from_room()
                if err:
                    raise RuntimeError(err)
            self.__devices = []
            err = self.power_off()
            if err:
                raise RuntimeError(err)
            self.__room = None
        except RuntimeError as err:
            errmsg = "Could not remove from room"
            self.error(err)
            return errmsg
        else:
            return None
    
    def stop(self) -> str:
        """
        Stops the controller. In essence, disconnects\n
        from the broker and stops listening to incoming topics.
        Must be implemented by subclass
        """
        pass

    def start(self) -> str:
        """
        Starts the controller. In essence, connects\n
        to the broker and starts listening to the incoming messages\n
        in the relevant topics
        """
        pass

    def get_room_id(self) -> str:
        """
        Returns the id of the room in which\n
        this controller is present
        """
        return self.__room.get_id()
    
    def get_device_by_id(self, device_id: str) -> Device:
        """
        Finds and returns the device object with given id\n
        `device_id` from the list of devices. Returns the\n
        device object if found, else returns `None`
        """
        try:
            for device in self.__devices:
                if device.get_id() == device_id:
                    return device
            err = "Device not found"
            raise ValueError(err)
        except ValueError as err:
            self.error(err)
            return None
        except RuntimeError as err:
            self.error(err)
            return None
    
    def get_all_device_ids(self) -> str:
        """
        Returns the ids of all devices of this controller\n
        concatenated with a comma separator.
        """
        device_ids = [device.get_id() for device in self.__devices]
        return ",".join(device_ids)
    
    def set_device_power(self, device_id: str, state: Literal) -> Literal:
        """
        Sets the power status of the device with id\n
        `device_id`. Returns corresponding operation status.
        """
        try:
            device: Device = self.get_device_by_id(device_id)
            if device:
                err = None
                if state == PowerStatus.OFF:
                    err = device.power_off()
                elif state == PowerStatus.ON:
                    err = device.power_on()
                
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def get_all_device_status(self) -> List[Dict[str, Any]]:
        """
        Returns the list of all status dictionaries of the devices of this controller.
        """
        statuses: List[Dict[str, Any]] = []

        for device in self.__devices:
            statuses.append(device.get_status_string)
        
        return statuses