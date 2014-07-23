import sfml as sf
import src.net as net
import src.const as const

from src.input_system import MouseHandler
from src.gui import Button
from src.rect import contains

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class FarmInterface:
    def __init__(self, client, user, input):
        self.client = client
        self.user = user # Can be student or teacher
        
        self.test_button = Button(0, 0, "button", 3, 3, input)
        
        self.buttons = []
        self.buttons.append(self.test_button)
    
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        for button in self.buttons:
            if mouse_button == sf.Mouse.LEFT and not contains(button.rectangle, sf.Vector2(x, y)):
                packet = net.Packet()
                packet.write(const.packet_request_place_item)
                packet.write("tree")
                packet.write(x)
                packet.write(y)
                self.client.send(packet)
            
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass
        
    # KEYBOARD
    def on_key_pressed(self, key_code):
        if key_code < 26 and key_code > 0: #only get the alphabet
            if keys[key_code] == 's':
                # Save user information
                packet = net.Packet()
                packet.write(const.packet_save)
                self.user.serialize(packet)
                # Save farm information
                packet.write(len(self.user.farm.land_items))
                for item in self.user.farm.land_items:
                    item.serialize(packet)
                # Send file
                self.client.send(packet)
    
    def on_key_released(self, key_code):
        pass
        
    def draw(self, target):
        target.draw(self.test_button.sprite)
