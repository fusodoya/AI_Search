from object_folder.object import *

class Stone(Object):
    cnt = 0

    def __init__(self, val, state):
        super().__init__()
        self.__val = val
        self.__state = state # 0 = free, 1 = on switch
        Stone.cnt += 1

    def print_info(self):
        super().__init__()
        print("Stone:")
        print("    Val: " + str(self.__val))
        print("    State: " + str(self.__state))


    def get_val(self):
        return self.__val

    def set_val(self, new_val):
        self.__val = new_val

    def is_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state
