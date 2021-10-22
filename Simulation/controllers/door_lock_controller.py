from typing import Any, Literal
from utilities import DoorLockOp
from devices import DoorLock
from base_classes import Controller
from utilities import DeviceType, OPStatus, PowerStatus, DoorLockStatus
from utilities import get_mqtt_com_topic
from utilities import get_mqtt_com_fail_topic
from utilities import get_mqtt_sub_topic, get_mqtt_unsub_topic
from utilities import MQTTConnection, StatusThread
import paho.mqtt.client as mqtt

class DoorLockController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.DOOR_LOCK)
        self.__running = False
        self.__client: MQTTConnection = None
        self.__status_thread: StatusThread = None
    
    def error(self, errmsg: str, lock: DoorLock = None) -> None:
        """
        Prints/logs error message
        """
        prefix = ""
        if lock:
            prefix = "DoorLockController for door lock {}->".format(
                lock.get_name()
            )
        else:
            prefix = "DoorLockController->"
        super().error(errmsg, prefix)
    
    def set_lock_state(self, lock_id: str, lock_state: Literal) -> Literal:
        """
        Sets the lock state of the door lock with device id\n
        as `lock_id`. Returns corresponding operation status.
        """
        try:
            lock: DoorLock = self.get_device_by_id(lock_id)
            if lock:
                err = lock.set_lock_state(lock_state)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def __on_message(self,
                    client: mqtt.Client,
                    userdata: Any,
                    msg: mqtt.MQTTMessage) -> None:
        message = str(msg.payload.decode('utf-8'))
        message = message.strip()
        message = message.split(" ")
        device_id = message[0]
        command = message[1]
        status = None
        if command == "OFF":
            status = self.set_device_power(device_id, PowerStatus.OFF)
        elif command == "ON":
            status = self.set_device_power(device_id, PowerStatus.ON)
        elif command == DoorLockOp.SET_LOCK.value:
            lock_state = message[2]
            if lock_state == "OFF":
                status = self.set_lock_state(device_id, DoorLockStatus.OFF)
            elif lock_state == "ON":
                status = self.set_lock_state(device_id, DoorLockStatus.ON)

        client.publish(
            topic=get_mqtt_com_fail_topic(
                device_id
            ),
            payload="{}/{}".format(command, OPStatus.FAILED.value),
            qos=1
        )
    
    def __on_subscribe(self,
                    client: mqtt.Client,
                    userdata: Any,
                    mid: Any,
                    granted_qos: int) -> None:
        client.publish(
            topic=get_mqtt_sub_topic(self),
            payload=self.get_all_device_ids(),
            qos=2
        )
    
    def __on_unsubscribe(self,
                    client: mqtt.Client,
                    userdata: Any,
                    mid: Any,
                    granted_qos: int) -> None:
        client.publish(
            topic=get_mqtt_unsub_topic(self),
            qos=2
        )

    def start(self) -> None:
        if not self.__running:
            self.__client = MQTTConnection(
                id=self.get_id(),
                topic=get_mqtt_com_topic(self),
                on_message=self.__on_message,
                on_subscribe=self.__on_subscribe,
                on_unsubscribe=self.__on_unsubscribe
            )
            errmsg = self.__client.start()
            if errmsg:
                self.error(errmsg)
            else:
                self.__running = True
            self.__status_thread = StatusThread(
                client=self.__client.get_client(),
                controller=self
            )
            self.__status_thread.start()
    
    def stop(self) -> None:
        if self.__running:
            self.__status_thread.stop()
            errmsg = self.__client.stop()
            if errmsg:
                self.error(errmsg)
            else:
                self.__running = False
    
    def is_running(self) -> bool:
        """
        Returns `True` if the controller is\n
        in running state i.e., connected to the broker,\n
        else returns `False`
        """
        return self.__running
