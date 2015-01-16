import sfml as sf
from src.states.state import ClientState

import src.net as net

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

class HomeFarmState(ClientState):
    def init(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
        # CONTROL WINDOW
        self.load_button = Button(sf.Vector2(0, 0), "button", input, "load")
        self.save_button = Button(sf.Vector2(0, 32), "button", input, "save")
        self.shop_button = Button(sf.Vector2(104, 0), "button", input, "shop")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, user.user_name, input)
        
        self.ctrl_window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), input)
        self.ctrl_window.add_child(self.load_button)
        self.ctrl_window.add_child(self.save_button)
        self.ctrl_window.add_child(self.shop_button)
        self.ctrl_window.add_child(self.textbox)
        
        self.gui_manager.add(self.ctrl_window)
        
        self.farm_items = [] # what to draw - trees, fences, etc.
        
    def handle_packet(self, packet):
        pass
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            print("left")
        
class GuestFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
        self.farm_items = [] # what to draw - trees, fences, etc.
        
    def handle_packet(self, packet):
        pass
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
