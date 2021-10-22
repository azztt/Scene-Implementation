from __future__ import annotations
from typing import List, Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from .controller import Controller
    from .device import Device
from utilities import Error
from .entity import Entity

class Room(Entity):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id)
        self.__controllers: List[Controller] = []
    
    def error(self, errmsg: str, prefix: str = "") -> None:
        """
        Prints/logs error message
        """
        print("{}Room {}: {}".format(prefix, self.name, errmsg))
    
    def add_controller(self, controller: Controller) -> str:
        """
        Adds the `controller` to this room's list\n
        of controllers. Returns `None` on success, else\n
        returns the error message
        """
        try:
            err = controller.place_in_room(self)
            if err:
                raise RuntimeError(err)
            self.__controllers.append(controller)
        except RuntimeError as err:
            errmsg = "Could not add controller to the room"
            self.error(err)
            return errmsg
        else:
            return None
    
    def remove_controller(self, controller: Controller) -> str:
        """
        Removes the `controller` from this room's list\n
        of controllers. The controller is stopped and all devices\n
        for that controller must be removed before\n
        stopping. Returns `None` on success, else\n
        returns the error message
        """
        try:
            err = controller.remove_from_room(self)
            if err:
                raise RuntimeError(err)
            self.__controllers.append(controller)
        except RuntimeError as err:
            errmsg = "Could not add controller to the room"
            self.error(err)
            return errmsg
        else:
            return None
    
    def __get_device_controller(self, type: Literal) -> Controller:
        """
        Checks and returns the controller of device type `type`\n
        is present in the room, else returns None.
        """
        for controller in self.__controllers:
            if controller.get_device_type() == type:
                return controller
        
        return None

    def add_device(self, device: Device) -> str:
        """
        Adds a new device to the room's relevant controller.\n
        Returns `None` on success, else error message.
        """
        try:
            controller = self.__get_device_controller(device.get_device_type())
            if not controller:
                err = "No controller of this type present. "
                err += "First, add a controller of this type to the room."
                raise RuntimeError(err)
            err = device.place_in_room(self)
            if err:
                raise RuntimeError(err)
            controller.add_device(device)
        except RuntimeError as err:
            if err[:13] == "No controller":
                return Error.NO_CONT.value
            errmsg = "Could not add device to the room"
            self.error(err)
            return errmsg
        else:
            return None
    
    def remove_device_by_id_type(self, device_id: str, type: Literal) -> str:
        """
        Removes the device with given id and type from the\n
        relevant controller of the room.\n
        Returns `None` on success, else error message.
        """
        try:
            controller = self.__get_device_controller(type)
            if not controller:
                err = "No controller of this type present."
                raise RuntimeError(err)
            err = controller.remove_device_by_id(device_id)
            if err:
                raise RuntimeError(err)
        except ValueError as err:
            self.error(err)
            return err
        except RuntimeError as err:
            errmsg = "Could not remove device with id '{}'".format(
                device_id
            )
            self.error(err)
            return errmsg
        else:
            return None
    
    def empty_room(self) -> str:
        """
        Removes all the devices and hence controllers from the room.\n
        All controllers are stopped before removing.\n
        Returns `None` on success, else an error message.
        """
        try:
            for controller in self.__controllers:
                err = controller.remove_from_room()
                if err:
                    raise RuntimeError(err)
            
            self.__controllers = []
        except RuntimeError as err:
            errmsg = "Could not remove all devices from the room."
            self.error(err)
            return errmsg
        else:
            return None