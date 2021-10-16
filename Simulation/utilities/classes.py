import uuid
from utilities import MQTT_SERVER
from uuid import uuid4

class MQTTConnection:
    def __init__(self, host: str) -> None:
        self.__topic = ""
    
    def get_topic(self) -> str:
        """
        Generates and returns the topic """
    
class IDClass:
    """
    Unique ID generator for different entitites
    """
    def __init__(self) -> None:
        self.__next_id = set()
    
    def new_id(self) -> int:
        """
        Returns new unique id
        """
        id = str(uuid4())
        while id in self.__next_id:
            id = str(uuid4())
        self.__next_id.add(id)
        return id