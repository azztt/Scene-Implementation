from base_classes import Device


class AirConditioner(Device):
    def __init__(self, name: str, id: int) -> None:
        super().__init__(name, id)
        
