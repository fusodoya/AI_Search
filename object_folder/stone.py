from object_folder.object import *

class Stone(Object):
    cnt = 0

    def __init__(self, val, state):
        super().__init__()
        self.val = val
        self.state = state # 0 = free, 1 = on switch
        Stone.cnt += 1
        self.id = Stone.cnt

    def print_info(self):
        print("Stone:")
        print("    Val: " + str(self.val))
        print("    State: " + str(self.state))


    def get_val(self):
        return self.val

    def set_val(self, new_val):
        self.val = new_val

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
