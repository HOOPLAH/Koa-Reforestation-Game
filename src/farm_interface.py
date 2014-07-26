import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.input_system import MouseHandler
from src.gui import Button
from src.rect import contains

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# FarmInterface draws all the buttons and the farm currently on-screen
class FarmInterface:
    def __init__(self, client, student, input):
        self.client = client
        self.student = student
        self.input = input
        self.input.add_mouse_handler(self)
        
        self.test_button = Button(0, 0, "button", 3, 3, input)
        
        self.buttons = []
        self.buttons.append(self.test_button)
        
        self.land_items = []
        self.current_farm = None # The farm we're currently drawing
    
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
        if button == sf.Mouse.LEFT and contains(self.test_button.rectangle, sf.Vector2(x, y)):
            packet = net.Packet()
            packet.write(const.packet_request_load_farm)
            packet.write(self.student.client_id)
            self.client.send(packet)
            
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
        points = sf.Text("0", res.font_8bit, 20)
        points.position = sf.Vector2(760, 0)
        points.string = str(self.student.points)
        target.draw(points)
        
        for button in self.buttons:
            button.draw(target)
        
        for item in self.land_items:
            item.draw(target)
