import sfml as sf
import src.net as net
import src.const as const

from src.states.state import ClientState

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

from src.rect import contains

class LoginState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
    def init(self):
        super().init()

        self.first_textbox = Textbox(sf.Vector2(0, 16), 256, "lucas", self.input)
        self.last_textbox = Textbox(sf.Vector2(0, 48), 256, "derego1", self.input)
        self.login_button = Button(sf.Vector2(124-48, 80), "button", self.input, "login")

        self.window = Window(sf.Vector2(272, 112), 256, 128, sf.Color(50, 50, 120, 255), self.input)
        self.window.add_child(self.login_button)
        self.window.add_child(self.first_textbox)
        self.window.add_child(self.last_textbox)

        self.gui_manager.add(self.window)
    
    def handle_packet(self, packet):
        packet_id = packet.read()
            
        if packet_id == const.PacketTypes.LOGIN:
            self.user.deserialize(packet)
            self.user.switch_state(const.GameStates.HOME_FARM)

    def on_mouse_button_pressed(self, mouse_button, x, y):
        super().on_mouse_button_pressed(mouse_button, x , y)
        
        if mouse_button == sf.Mouse.LEFT: # login button pressed
            if contains(self.login_button.local_bounds, sf.Vector2(x, y)):
                login_packet = net.Packet()
                login_packet.write(const.PacketTypes.LOGIN)
                login_packet.write(self.first_textbox.last_text) # username
                login_packet.write(self.last_textbox.last_text) # password
                self.client.send(login_packet)
            
