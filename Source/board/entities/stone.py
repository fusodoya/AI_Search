from .entity_interface import EntityInterface

class Stone(EntityInterface):
    __stones_count = 0
    
    def __init__(self, is_on_switch: bool, weight: int):
        super().__init__(is_on_switch)
        self.__weight = weight
        
        Stone.__stones_count += 1
        self.__id = Stone.__stones_count

    def reset():
        Stone.__stones_count = 0
    
    def print_info(self):
        super().print_info()
        print("[+] Stone:")
        print("\tweight: ", self.weight)
        print("\tis_on_switch: ", self.is_on_switch)
    
    @property  
    def id(self) -> int:
        return self.__id
    
    @property   
    def weight(self) -> int:
        return self.__weight
    
    @weight.setter
    def weight(self, new_weight):
        self.__weight = new_weight
