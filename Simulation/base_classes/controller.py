from typing import List, Literal
from device import Device
from room import Room

class Controller(Device):
    def __init__(self, name: str, id: str, type: Literal) -> None:
        super().__init__(name, id, type)
        self.__room: Room = None
        self.__devices: List[Device] = []
    
    def __error(self, errmsg: str, prefix) -> None:
        """
        Prints/logs error message
        """
        prefix = prefix + "Controller->"
        print("{}Controller {} in Room {}: {}".format(
            prefix, self.name, 
            self.__room.get_name() if self.__room else "None",
            errmsg
        ))
    
    def add_device(self, device: Device) -> str:
        """
        Adds a new device to this controller's device list.\n
        Return `None` on success else and error message.
        """
        try:
            self.__devices.append(device)
        except RuntimeError as err:
            errmsg = "Could not add device to the controller"
            self.__error(err)
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
            self.__error(err)
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
            self.__error(err)
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
            self.__error(err)
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