from typing import Any, Literal
from utilities import FanOp
from devices import Fan
from base_classes import Controller
from utilities import DeviceType, OPStatus, PowerStatus
from utilities import get_mqtt_com_topic
from utilities import get_mqtt_com_ack_topic
from utilities import get_mqtt_sub_topic, get_mqtt_unsub_topic
from utilities import MQTTConnection, StatusThread
import paho.mqtt.client as mqtt

class FanController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.FAN)
        self.__running = False
        self.__client: MQTTConnection = None
        self.__status_thread: StatusThread = None
    
    def error(self, errmsg: str, fan: Fan = None) -> None:
        """
        Prints/logs error message
        """
        prefix = ""
        if fan:
            prefix = "FanController for fan {}->".format(
                fan.get_name()
            )
        else:
            prefix = "FanController->"
        super().error(errmsg, prefix)

    def set_speed(self, fan_id: str, level: int) -> Literal:
        """
        Sets the speed level of the fan with device id\n
        as `fan_id`. Returns corresponding operation status.
        """
        try:
            fan: Fan = self.get_device_by_id(fan_id)
            if fan:
                err = fan.set_speed_level(level)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_status(self, fan_id: str, status_string: str) -> Literal:
        """
        Sets the status parameters based on a string\n
        of multiple parameters from server. Returns\n
        corresponding operation status.
        """
        try:
            fan: Fan = self.get_device_by_id(fan_id)
            if fan:
                err = fan.set_from_param_string(status_string)
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
        if device_id in self.get_all_device_ids().split(","):
            command = message[1]
            status = None
            if command == "status":
                status_string = message[2]
                status = self.set_status(device_id, status_string)
            elif command == "OFF":
                status = self.set_device_power(device_id, PowerStatus.OFF)
            elif command == "ON":
                status = self.set_device_power(device_id, PowerStatus.ON)
            elif command == FanOp.SET_SPEED.value:
                level = int(message[2])
                status = self.set_speed(device_id, level)
            
            if status == OPStatus.FAILED:
                client.publish(
                    topic=get_mqtt_com_ack_topic(
                        device_id
                    ),
                    payload="{}/FAILED".format(command),
                    qos=1
                )
            else:
                client.publish(
                    topic=get_mqtt_com_ack_topic(
                        device_id
                    ),
                    payload="{}/SUCCESS".format(command),
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
            payload=self.get_all_device_ids(),
            qos=2
        )

    def start(self) -> None:
        if not self.__running:
            self.__client = MQTTConnection(
                id=self.get_id(),
                topic=get_mqtt_com_topic(self),
                on_message=self.__on_message,
                on_subscribe=self.__on_subscribe,
                on_unsubscribe=self.__on_unsubscribe,
                will_payload=self.get_all_device_ids()
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
