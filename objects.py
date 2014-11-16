class Switch:
    def __init__(self, x, y, targets):
        self.position = (x, y)
        self.pressed = False
        self.toggle_changed = False
        self.targets = targets
        
    def step_on(self):
        if not self.pressed:
            self.pressed = True
            self.toggle_changed = True
            print "Switch pressed!"
        
    def step_off(self):
        if self.pressed:
            self.pressed = False
            self.toggle_changed = True
            print "Switch off!"