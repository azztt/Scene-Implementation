from typing import Any, Literal, Tuple
from utilities import CLightOp
from devices import ColorLight
from base_classes import Controller
from utilities import DeviceType, OPStatus, PowerStatus
from utilities import get_mqtt_com_topic
from utilities import get_mqtt_com_ack_topic
from utilities import get_mqtt_sub_topic, get_mqtt_unsub_topic
from utilities import MQTTConnection, StatusThread
import paho.mqtt.client as mqtt

class ColorLightController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.COL_LIGHT)
        self.running = False
        self.client: MQTTConnection = None
        self.status_thread: StatusThread = None
    
    def error(self, errmsg: str, clight: ColorLight = None) -> None:
        """
        Prints/logs error message
        """
        prefix = ""
        if clight:
            prefix = "ColorLightController for color light {}->".format(
                clight.get_name()
            )
        else:
            prefix = "ColorLightController->"
        super().error(errmsg, prefix)

    def set_color(self, clight_id: str, color: Tuple[int, int , int]) -> Literal:
        """
        Sets the color of the color light with device id\n
        as `clight_id`. Returns corresponding operation status.
        """
        try:
            clight: ColorLight = self.get_device_by_id(clight_id)
            if clight:
                err = clight.set_color(color)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_brightness(self, light_id: str, level: int) -> Literal:
        """
        Sets the brightness of the light with device id\n
        as `light_id`. Returns corresponding operation status.
        """
        try:
            light: ColorLight = self.get_device_by_id(light_id)
            if light:
                err = light.set_brightness(level)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_status(self, light_id: str, status_string: str) -> Literal:
        """
        Sets the status parameters based on a string\n
        of multiple parameters from server. Returns\n
        corresponding operation status.
        """
        try:
            light: ColorLight = self.get_device_by_id(light_id)
            if light:
                err = light.set_from_param_string(status_string)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def on_message(self,
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
            elif command == CLightOp.SET_BRIGHT.value:
                level = int(message[2])
                status = self.set_brightness(device_id, level)
            elif command == CLightOp.SET_COLOR.value:
                # of format '(R,G,B)'
                color_string = message[2]
                color_string = color_string[1:-1]
                color_codes = color_string.split(",")
                color = list(map(int, color_codes))
                color = tuple(color)
                status = self.set_color(device_id, color)
            
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
    
    def on_subscribe(self,
                    client: mqtt.Client,
                    userdata: Any,
                    mid: Any,
                    granted_qos: int) -> None:
        client.publish(
            topic=get_mqtt_sub_topic(self),
            payload=self.get_all_device_ids(),
            qos=2
        )
    
    def on_unsubscribe(self,
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
        if not self.running:
            self.client = MQTTConnection(
                id=self.get_id(),
                topic=get_mqtt_com_topic(self),
                on_message=self.on_message,
                on_subscribe=self.on_subscribe,
                on_unsubscribe=self.on_unsubscribe,
                will_payload=self.get_all_device_ids()
            )
            errmsg = self.client.start()
            if errmsg:
                self.error(errmsg)
            else:
                self.running = True
            self.status_thread = StatusThread(
                client=self.client.get_client(),
                controller=self
            )
            self.status_thread.start()
    
    def stop(self) -> None:
        if self.running:
            self.status_thread.stop()
            errmsg = self.client.stop()
            if errmsg:
                self.error(errmsg)
            else:
                self.running = False
                self.client = None
                self.status_thread = None
    
    def is_running(self) -> bool:
        """
        Returns `True` if the controller is\n
        in running state i.e., connected to the broker,\n
        else returns `False`
        """
        return self.running
