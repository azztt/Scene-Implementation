from __future__ import annotations
from threading import Thread
from time import sleep, time
from types import FunctionType
from typing import Any, TYPE_CHECKING, Dict, List
from .constants import MQTT_SERVER, MQTT_QOS
from .constants import MQTT_PORT, MQTT_WILL_TOPIC
from .constants import STATUS_CRON_TIME
from uuid import uuid4
import paho.mqtt.client as mqtt
if TYPE_CHECKING:
    from base_classes import Controller
from time import perf_counter
from simulation.sim_constants import DEVICE_STATUS
import json

class MQTTConnection:
    def __init__(self,
                id: str,
                topic: str,
                on_subscribe: FunctionType,
                on_unsubscribe: FunctionType,
                on_message: FunctionType,
                will_payload: str) -> None:
        self.__client_id = id
        self.__topic = topic
        self.__client = mqtt.Client(
            client_id=self.__client_id,
            clean_session=False,
        )
        self.__on_unsubscribe = on_unsubscribe
        self.__on_subscribe = on_subscribe
        self.__on_message = on_message
        self.__will_payload = will_payload
    
    def __on_connect(self,
                client: mqtt.Client,
                userdata: Any,
                flags: Any,
                rc: Any) -> None:
        print("Controller {} connected with result code {}".format(
            self.__client_id,
            rc
        ))
        (res, _) = client.subscribe(
            topic=self.__topic,
            qos=MQTT_QOS
        )
        while res > 0:
            (res, _) = client.subscribe(
                topic=self.__topic,
                qos=MQTT_QOS
            )
    
    def __on_disconnect(self,
                        client: mqtt.Client,
                        userdata: Any,
                        rc: Any) -> None:
        print("Controller {} disconnected with result code {}".format(
            self.__client_id,
            rc
        ))
    
    def get_client(self) -> mqtt.Client:
        """
        Returns the client object of this connection.
        """
        return self.__client
    
    def start(self) -> str:
        """
        Starts the client connection to the broker.\n
        Returns `None` on successful connection,\n
        returns an error message.
        """
        try:
            self.__client.on_connect = self.__on_connect
            self.__client.on_disconnect = self.__on_disconnect
            self.__client.on_message = self.__on_message
            self.__client.on_subscribe = self.__on_subscribe
            self.__client.on_unsubscribe = self.__on_unsubscribe
            self.__client.will_set(
                topic=MQTT_WILL_TOPIC,
                payload=self.__will_payload,
            )
            self.__client.connect(
                host=MQTT_SERVER,
                port=MQTT_PORT
            )
            self.__client.loop_start()
        except RuntimeError:
            errmsg = "Could not start mqtt connection"
            return errmsg
        else:
            return None
    
    def stop(self) -> str:
        """
        Stops the client connection to the broker.\n
        Returns `None` on successful connection,\n
        returns an error message.
        """
        try:
            if self.__client.is_connected():
                self.__client.unsubscribe(self.__topic)
                self.__client.loop_stop()
                self.__client.disconnect()
        except RuntimeError:
            errmsg = "Could not disconnect mqtt connection"
            return errmsg
        else:
            return None

class IDClass:
    """
    Unique ID generator for different entitites
    """
    def __init__(self) -> None:
        self.__next_id = set()
    
    def new_id(self) -> str:
        """
        Returns new unique id
        """
        id = str(uuid4())
        while id in self.__next_id:
            id = str(uuid4())
        self.__next_id.add(id)
        return id

class StatusThread(Thread):
    def __init__(self, client: mqtt.Client, controller: Controller) -> None:
        self.__client = client
        self.__controller = controller
        self.__on = False
    
    def stop(self) -> None:
        self.__on = False
    
    def run(self) -> None:
        self.__on = True

        while(self.__on):
            t1 = perf_counter()

            statuses: List[Dict[str, Any]] = self.__controller.get_all_device_status()

            deviceStatus = {
                "statuses": statuses
            }

            # for status in statuses:
            #     self.__client.publish(
            #         topic="/".join([DEVICE_STATUS, status["type"]]),
            #         payload=json.dumps(status),
            #         qos=1
            #     )
            
            self.__client.publish(
                topic=DEVICE_STATUS,
                payload=json.dumps(deviceStatus),
                qos=1
            )

            # print device statuses to console for testing
            print("Updated device statuses:")
            print(deviceStatus)
            
            t2 = perf_counter()

            diff = t2-t1
            diff = STATUS_CRON_TIME - diff
            if diff > 0:
                sleep(diff)
            else:
                sleep(2)