import sfml as sf
from enum import IntEnum

from src.input_system import InputSystem
from src.GUI.gui_manager import GUIManager
from src.user import User

from src.packet_manager import ServerPacketManager

class GameStates(IntEnum):
	LOGIN = 0
	HOME_FARM = 1
	GUEST_FARM = 2
	SHOP = 3
	STATISTICS = 4

class ClientState:
    def __init__(self, client, input, gui_manager, user):
        self.client = client
        self.input = input
        self.gui_manager = gui_manager
        self.user = user

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
        
class ServerGameStates(IntEnum):
    LOAD = 0
    GAME = 1
        
class ServerState:
    def __init__(self, server, packet_manager, users):
        self.server = server
        self.packet_manager = packet_manager
        
        self.users = users # all registered users, called by username
        self.connected_users = {} # all users online, called by client_id
    
    def handle_packet(self, client_id, packet):
        pass
    
    def on_connect(self, client_id):
        pass
        
    def on_disconnect(self, client_id):
        pass
        
    def update(self, dt):
        pass
