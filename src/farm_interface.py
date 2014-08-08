import sfml as sf
import src.net as net
import src.const as const
import src.res as res

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.messagebox import MessageBox
from src.GUI.gui_manager import GUIManager

from src.interface import Interface
from src.rect import contains

# FarmInterface draws all the buttons and the farm currently on-screen
class FarmInterface(Interface):
    def __init__(self, client, student, farm, input):
        super().__init__(client, student, input)
        
        self.load_button = Button(sf.Vector2(0, 0), "button", input, "load")
        self.save_button = Button(sf.Vector2(0, 32), "button", input, "save")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, "find user", input)
        
        self.window = Window(sf.Vector2(0, 0), 256, 256, sf.Color(50, 50, 120, 255), input)
        self.window.add_child(self.load_button)
        self.window.add_child(self.save_button)
        self.window.add_child(self.textbox)
        
        self.gui_manager.add(self.window)
        
        self.current_farm = farm # The farm we're currently drawing
        
    def mouse_over_window(self, x, y): # Hack 
        for i in range(0, len(self.gui_manager.children)):
            if contains(self.gui_manager.children[i].local_bounds, sf.Vector2(x, y)):
                return True
            else:
                continue
            
        return False
    
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if not self.mouse_over_window(x, y):
                packet = net.Packet()
                packet.write(const.packet_request_place_item)
                packet.write("tree")
                packet.write(x)
                packet.write(y)
                self.client.send(packet)
                
        if mouse_button == sf.Mouse.RIGHT:
            for item in reversed(self.current_farm.land_items):
                if contains(item.local_bounds, sf.Vector2(x, y)):
                    self.current_farm.land_items.remove(item)
                    break # only delete one tree
            
    def on_mouse_button_released(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if contains(self.load_button.local_bounds, sf.Vector2(x, y)):
                packet = net.Packet()
                packet.write(const.packet_request_load_farm)
                packet.write(self.textbox.text.string) # send the name 
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
            
    def draw(self, target):
        super().draw(target)
        
        for item in self.current_farm.land_items:
            item.draw(target)