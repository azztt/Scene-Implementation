class Entity:
    """
    Most basic entity with a name and id.\n
    Once instantiated, only `name` can be changed.\n
    `id` of the cannot be changed.
    """
    def __init__(self, name: str, id: str) -> None:
        self.__name = name if len(name) <= 100 else name[:100]
        self.__id = id
    
    def get_name(self) -> str:
        """
        Returns entity's name
        """
        return self.__name
    
    def set_name(self, name: str) -> None:
        """
        Sets entity's name to `name`.\n
        """
        self.__name = name
    
    def get_id(self) -> str:
        return self.__id