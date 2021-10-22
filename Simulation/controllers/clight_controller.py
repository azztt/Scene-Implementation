from typing import Any, Literal, Tuple
from utilities import CLightOp
from devices import ColorLight
from base_classes import Controller
from utilities import DeviceType, OPStatus, PowerStatus
from utilities import get_mqtt_com_topic
from utilities import get_mqtt_com_fail_topic
from utilities import get_mqtt_sub_topic, get_mqtt_unsub_topic
from utilities import MQTTConnection, StatusThread
import paho.mqtt.client as mqtt

class ColorLightController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.COL_LIGHT)
        self.__running = False
        self.__client: MQTTConnection = None
        self.__status_thread: StatusThread = None
    
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
                topic=get_mqtt_com_fail_topic(
                    device_id
                ),
                payload="{}/FAILED".format(command),
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
