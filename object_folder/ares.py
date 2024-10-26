from object_folder.object import *

class Ares(Object):
    def __init__(self, state):
        super().__init__()
        self.state = state # False = free, True = on switch
        self.id = 0

    def print_info(self):
        print("Ares:")
        print("    State: " + str(self.state))

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
