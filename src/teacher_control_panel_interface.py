import sfml as sf
import src.net as net
import src.const as const

from src.interface import Interface
from src.rect import contains

from src.GUI.label import Label
from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

class TeacherControlPanelInterface(Interface):
    def __init__(self, client, user, input):
        super().__init__(client, user, input)
        
        self.search_window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), input)
        self.search_label = Label(sf.Vector2(103.5, 0), "Search", input, sf.Color.WHITE)
        self.search_textbox = Textbox(sf.Vector2(0, 37), 256, "lucas derego", input)
        self.find_button = Button(sf.Vector2(124-48, 69), "button", input, "find")
        
        self.search_window.add_child(self.search_label)
        self.search_window.add_child(self.search_textbox)
        self.search_window.add_child(self.find_button)
        
        self.control_window = Window(sf.Vector2(260, 0), 256, 128, sf.Color(50, 50, 120, 255), input)
        self.control_label = Label(sf.Vector2(103.5, 0), "Control", input, sf.Color.WHITE)
        self.points_textbox = Textbox(sf.Vector2(0, 37), 256, "add points", input)
        self.add_button = Button(sf.Vector2(16, 69), "button", input, "add")
        
        self.control_window.add_child(self.control_label)
        self.control_window.add_child(self.points_textbox)
        self.control_window.add_child(self.add_button)
        
        self.gui_manager.add(self.search_window)
        self.gui_manager.add(self.control_window)
        
        self.current_farm = user.farm
        
    def on_mouse_button_released(self, mouse_button, x, y):
        super().on_mouse_button_released(mouse_button, x, y)
        
        if mouse_button == sf.Mouse.LEFT:
            if contains(self.find_button.local_bounds, sf.Vector2(x, y)):
                packet = net.Packet()
                packet.write(const.packet_request_load_farm)
                packet.write(self.search_textbox.text.string) # send the name 
                self.client.send(packet)
            elif contains(self.add_button.local_bounds, sf.Vector2(x, y)):
                packet = net.Packet()
                packet.write(const.packet_add_points)
                packet.write(self.search_textbox.text.string) # name of student
                packet.write(int(self.points_textbox.text.string)) # amount of points to add
                self.client.send(packet)
                
    def on_mouse_moved(self, position, move):
        if not self.mouse_over_window(position.x, position.y):
            if self.mouse_state == 'down': # mouse is down
                self.view.move(-move.x, -move.y)
            
    def draw(self, target):
        target.view = self.view
        
        for item in self.current_farm.land_items:
            item.draw(target)
            
        target.view = target.default_view
        super().draw(target)