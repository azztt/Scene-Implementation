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
from .constants import DEVICE_STATUS
import json

class MQTTConnection:
    def __init__(self,
                id: str,
                topic: str,
                on_subscribe: FunctionType,
                on_unsubscribe: FunctionType,
                on_message: FunctionType,
                will_payload: str) -> None:
        self.client_id = id
        self.topic = topic
        self.client = mqtt.Client(
            client_id=self.client_id,
            clean_session=False,
        )
        self.on_unsubscribe = on_unsubscribe
        self.on_subscribe = on_subscribe
        self.on_message = on_message
        self.will_payload = will_payload
    
    def on_connect(self,
                client: mqtt.Client,
                userdata: Any,
                flags: Any,
                rc: Any) -> None:
        print("Controller {} connected with result code {}".format(
            self.client_id,
            rc
        ))
        (res, _) = client.subscribe(
            topic=self.topic,
            qos=MQTT_QOS
        )
        while res > 0:
            (res, _) = client.subscribe(
                topic=self.topic,
                qos=MQTT_QOS
            )
    
    def on_disconnect(self,
                        client: mqtt.Client,
                        userdata: Any,
                        rc: Any) -> None:
        print("Controller {} disconnected with result code {}".format(
            self.client_id,
            rc
        ))
    
    def get_client(self) -> mqtt.Client:
        """
        Returns the client object of this connection.
        """
        return self.client
    
    def start(self) -> str:
        """
        Starts the client connection to the broker.\n
        Returns `None` on successful connection,\n
        returns an error message.
        """
        try:
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            self.client.on_subscribe = self.on_subscribe
            self.client.on_unsubscribe = self.on_unsubscribe
            self.client.will_set(
                topic=MQTT_WILL_TOPIC,
                payload=self.will_payload,
            )
            self.client.connect(
                host=MQTT_SERVER,
                port=MQTT_PORT
            )
            self.client.loop_start()
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
            if self.client.is_connected():
                self.client.unsubscribe(self.topic)
                self.client.loop_stop()
                self.client.disconnect()
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
        self.next_id = set()
    
    def new_id(self) -> str:
        """
        Returns new unique id
        """
        id = str(uuid4())
        while id in self.next_id:
            id = str(uuid4())
        self.next_id.add(id)
        return id

class StatusThread(Thread):
    def __init__(self, client: mqtt.Client, controller: Controller) -> None:
        super().__init__()
        self.client = client
        self.controller = controller
        self.on = False
    
    def stop(self) -> None:
        self.on = False
        self.client = None
    
    def run(self) -> None:
        self.on = True

        while(self.on):
            t1 = perf_counter()

            statuses: List[Dict[str, Any]] = self.controller.get_all_device_status()

            deviceStatus = {
                "statuses": statuses
            }

            # for status in statuses:
            #     self.client.publish(
            #         topic="/".join([DEVICE_STATUS, status["type"]]),
            #         payload=json.dumps(status),
            #         qos=1
            #     )
            
            self.client.publish(
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