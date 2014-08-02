import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.gui import Button
from src.gui import Textbox
from src.gui import Window
from src.interface import Interface
from src.rect import contains

# FarmInterface draws all the buttons and the farm currently on-screen
class FarmInterface(Interface):
    def __init__(self, client, student, farm, input):
        super().__init__(client, student, input)
        
        self.load_button = Button(sf.Vector2(0, 0), "button", 3, 3, input)
        self.save_button = Button(sf.Vector2(0, 32), "button", 3, 3, input)
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, "test", input)
        
        self.window = Window(sf.Vector2(0, 0), 256, 256, sf.Color(50, 50, 120, 255), input)
        self.window.add_child(self.load_button)
        self.window.add_child(self.save_button)
        self.window.add_child(self.textbox)
        
        self.current_farm = farm # The farm we're currently drawing
        
    def mouse_over_buttons(self, x, y): # Hack so the buttons work together
        i = 0 # the amount of buttons not pressed
        button_pressed = False
        while (i < len(self.window.children)) and button_pressed == False:
            if contains(self.window.vertices.bounds, sf.Vector2(x, y)) == False:
                i+=1
            else:
                button_pressed = True
                
        return button_pressed
    
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if not self.mouse_over_buttons(x, y):
                packet = net.Packet()
                packet.write(const.packet_request_place_item)
                packet.write("tree")
                packet.write(x)
                packet.write(y)
                self.client.send(packet)
                
        if mouse_button == sf.Mouse.RIGHT:
            for item in self.current_farm.land_items:
                print("DELETE")
                if contains(item.local_bounds, sf.Vector2(x, y)):
                    self.current_farm.land_items.remove(item)
            
    def on_mouse_button_released(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if contains(self.load_button.local_bounds, sf.Vector2(x, y)) and self.current_farm != self.student.farm:
                packet = net.Packet()
                packet.write(const.packet_request_load_farm)
                packet.write(self.student.client_id)
                self.client.send(packet)
            if contains(self.save_button.local_bounds, sf.Vector2(x, y)):
                # Save user information
                packet = net.Packet()
                packet.write(const.packet_save)
                self.student.serialize(packet)
                # Save farm information
                packet.write(len(self.current_farm.land_items))
                for item in self.current_farm.land_items:
                    item.serialize(packet)
                # Send file
                self.client.send(packet)
        
    def update(self, dt):
        self.window.update(dt)
            
    def draw(self, target):
        self.window.draw(target)
        
        for item in self.current_farm.land_items:
            item.draw(target)