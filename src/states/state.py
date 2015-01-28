import sfml as sf

from src.input_system import InputSystem
from src.GUI.gui_manager import GUIManager
from src.user import User

from src.packet_manager import ServerPacketManager

class ClientState:
    def __init__(self, client, input, gui_manager, user):
        self.client = client
        self.input = input
        self.gui_manager = gui_manager
        self.user = user
        
        self.mouse_state = 'up'
        
    def init(self):
        self.input.add_key_handler(self)
        self.input.add_text_handler(self)
        self.input.add_mouse_handler(self)
        
        self.client.add_handler(self)

    def handle_packet(self, packet):
        pass

    def render(self, target):
    	self.gui_manager.draw(target)

    def update(self, dt):
    	self.gui_manager.update(dt)

    # KEYBOARD
    def on_key_pressed(self, key_code):
        pass

    def on_key_released(self, key_code):
        pass
        
    # TEXT
    def on_text_entered(self, unicode):
        pass
        
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.mouse_state = 'down'

    def on_mouse_button_released(self, button, x, y):
        self.mouse_state = 'up'
            
    def on_mouse_moved(self, position, move):
        pass
        
    def on_mouse_wheel_moved(self, delta, position):
        pass
