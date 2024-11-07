from .entity_interface import EntityInterface

class Ares(EntityInterface):
    def __init__(self, is_on_switch):
        super().__init__(is_on_switch)
        self.__id = 0
    
    def print_info(self):
        super().print_info()
        print("[+] Ares:")
        print("\tis_on_switch: ", self.is_on_switch)
    
    @property
    def id(self) -> int:
        return self.__id
