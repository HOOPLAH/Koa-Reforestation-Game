import sfml as sf
import src.net as net
import src.const as const

#from src.farm import FarmLandItem
from src.input_system import MouseHandler

class FarmInterface:
    def __init__(self, client):
        self.client = client
        
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