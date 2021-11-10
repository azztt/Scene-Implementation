from typing import Any, Dict, Literal
from utilities import ACOp, PowerStatus
from utilities import ACFanSpeed, ACMode, ACSwingState
from devices import AirConditioner
from base_classes import Controller
from utilities import DeviceType, OPStatus
from utilities import get_mqtt_com_topic
from utilities import get_mqtt_com_ack_topic
from utilities import get_mqtt_sub_topic, get_mqtt_unsub_topic
from utilities import MQTTConnection, StatusThread
import paho.mqtt.client as mqtt

class ACController(Controller):
    def __init__(self, name: str, id: str) -> None:
        super().__init__(name, id, DeviceType.AC)
        self.running = False
        self.client: MQTTConnection = None
        self.status_thread: StatusThread = None
    
    def error(self, errmsg: str, ac: AirConditioner = None) -> None:
        """
        Prints/logs error message
        """
        prefix = ""
        if ac:
            prefix = "ACController for AC {}->".format(
                ac.get_name()
            )
        else:
            prefix = "ACController->"
        super().error(errmsg, prefix)
    
    def set_temp(self, ac_id: str, temp: int) -> Literal:
        """
        Sets the temperature of the AC with device id\n
        as `ac_id`. Returns corresponding operation status.
        """
        try:
            ac: AirConditioner = self.get_device_by_id(ac_id)
            if ac:
                err = ac.set_current_temp(temp)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_fan_speed(self, ac_id: str, level: Literal) -> Literal:
        """
        Sets the fan speed of the AC with device id\n
        as `ac_id`. Returns corresponding operation status.
        """
        try:
            ac: AirConditioner = self.get_device_by_id(ac_id)
            if ac:
                err = ac.set_fan_speed(level)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_swing(self, ac_id: str, state: Literal) -> Literal:
        """
        Sets the swing state of the AC with device id\n
        as `ac_id`. Returns corresponding operation status.
        """
        try:
            ac: AirConditioner = self.get_device_by_id(ac_id)
            if ac:
                err = ac.set_swing(state)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_mode(self, ac_id: str, mode: Literal) -> Literal:
        """
        Sets the mode of the AC with device id\n
        as `ac_id`. Returns corresponding operation status.
        """
        try:
            ac: AirConditioner = self.get_device_by_id(ac_id)
            if ac:
                err = ac.set_mode(mode)
                if err:
                    return OPStatus.FAILED
            else:
                return OPStatus.FAILED
        except RuntimeError as err:
            self.error(err)
            return OPStatus.FAILED
        else:
            return OPStatus.SUCCESS
    
    def set_status(self, ac_id: str, status_string: str) -> Literal:
        """
        Sets the status parameters based on a string\n
        of multiple parameters from server. Returns\n
        corresponding operation status.
        """
        try:
            ac: AirConditioner = self.get_device_by_id(ac_id)
            if ac:
                err = ac.set_from_param_string(status_string)
                if err:
                    print("ac status set error {}".format(err))
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
            elif command == ACOp.SET_TEMP.value:
                temp = int(message[2])
                status = self.set_temp(device_id, temp)
            elif command == ACOp.SET_FAN_SPEED.value:
                level = message[2]
                if level == "LOW":
                    status = self.set_fan_speed(device_id, ACFanSpeed.LOW)
                elif level == "MID":
                    status = self.set_fan_speed(device_id, ACFanSpeed.MID)
                elif level == "HIGH":
                    status = self.set_fan_speed(device_id, ACFanSpeed.HIGH)
            elif command == ACOp.SET_SWING.value:
                state = message[2]
                if state == "OFF":
                    status = self.set_swing(device_id, ACSwingState.OFF)
                elif state == "ON":
                    status = self.set_swing(device_id, ACSwingState.ON)
            elif command == ACOp.SET_MODE.value:
                mode = message[2]
                if mode == "FAN":
                    status = self.set_mode(device_id, ACMode.FAN)
                elif mode == "COOL":
                    status = self.set_mode(device_id, ACMode.COOL)
                elif mode == "DRY":
                    status = self.set_mode(device_id, ACMode.DRY)

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
