import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

from src.interface import Interface
from src.rect import contains

class LoginInterface(Interface):
    def __init__(self, client, input):
        super().__init__(client, None, input)
        
        self.first_textbox = Textbox(sf.Vector2(0, 16), 256, "lucas", input)
        self.last_textbox = Textbox(sf.Vector2(0, 48), 256, "derego", input)
        self.login_button = Button(sf.Vector2(124-48, 80), "button", input, "login")

        self.window = Window(sf.Vector2(272, 112), 256, 128, sf.Color(50, 50, 120, 255), input)
        self.window.add_child(self.login_button)
        self.window.add_child(self.first_textbox)
        self.window.add_child(self.last_textbox)
        
        self.gui_manager.add(self.window)
            
    def on_mouse_button_released(self, button, x, y):
        if button == sf.Mouse.LEFT:
            if contains(self.login_button.local_bounds, sf.Vector2(x, y)):
                first_name = self.first_textbox.text.string
                last_name = self.last_textbox.text.string
                
                packet = net.Packet()
                packet.write(const.packet_login)
                packet.write(first_name)
                packet.write(last_name)
                self.client.send(packet)
                self.client.update()
                
    def on_mouse_wheel_moved(self, delta, position):
        print(delta)