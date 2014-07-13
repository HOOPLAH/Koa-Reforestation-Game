import sfml as sf
import src.net as net
import src.const as const

from src.input_system import MouseHandler

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class FarmInterface:
    def __init__(self, client, student):
        self.client = client
        self.student = student
    
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            packet = net.Packet()
            packet.write(const.packet_request_place_item)
            packet.write(0)
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
                packet = net.Packet()
                packet.write(const.packet_save)
                self.student.serialize(packet)
                self.client.send(packet)
    
    def on_key_released(self, key_code):
        pass
    