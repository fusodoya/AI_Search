from object_folder.object import *

class Ares(Object):
    def __init__(self, state):
        super().__init__()
        self.__state = state # False = free, True = on switch

    def print_info(self):
        super().__init__()
        print("Ares:")
        print("    State: " + str(self.__state))

    def is_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state
