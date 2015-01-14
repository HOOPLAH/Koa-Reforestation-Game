from src.states.state import ClientState

import src.net as net

class HomeFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
        self.items = [] # what to draw
        
    def handle_packet(self, packet):
        pass
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        print("left")
        
class GuestFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
    def handle_packet(self, packet):
        pass
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
