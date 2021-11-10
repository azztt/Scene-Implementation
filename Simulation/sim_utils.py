from typing import Literal
import paho.mqtt.client as mqtt

def sim_acknowledge(client: mqtt.Client, topic: str, status: Literal) -> None:
    client.publish(
        topic="{}/ack".format(topic),
        payload=status,
        qos=2
    )