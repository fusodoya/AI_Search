from abc import ABC, abstractmethod

class EntityInterface(ABC):
    def __init__(self, is_on_switch: bool):
        super().__init__()
        
        self.__validate_boolean(is_on_switch)
        self.__is_on_switch = is_on_switch
    
    @abstractmethod
    def print_info(self):
        pass
    
    @property
    @abstractmethod
    def id(self) -> int:
        pass
    
    @property
    def is_on_switch(self) -> bool:
        return self.__is_on_switch
    
    @is_on_switch.setter
    def is_on_switch(self, new_value: bool):
        self.__validate_boolean(new_value)
        self.__is_on_switch = new_value
    
    def __validate_boolean(self, value):
        if not isinstance(value, bool):
            raise ValueError("Must be boolean.")
