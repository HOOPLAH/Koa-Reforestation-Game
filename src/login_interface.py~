import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.gui import Button
from src.gui import Textbox
from src.gui import Window
from src.interface import Interface
from src.rect import contains

class LoginInterface(Interface):
    def __init__(self, client, input):
        super().__init__(client, input)
        
        self.first_textbox = Textbox(sf.Vector2(272, 142), 256, input)
        self.last_textbox = Textbox(sf.Vector2(272, 174), 256, input)
        self.login_button = Button(sf.Vector2(304, 206), "button", 3, 3, input)
        
        self.window = Window(sf.Vector2(272, 112), 256, 64, sf.Color(50, 50, 120, 255), input)
        self.window.add_child(self.login_button)
        self.window.add_child(self.first_textbox)
        self.window.add_child(self.last_textbox)
            
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
                
    def update(self, dt):
        self.window.update(dt)
        
    def draw(self, target):
        self.window.draw(target)