import sfml as sf
from src.states.state import ClientState

import src.net as net
import src.const as const
import src.res as res
from src.rect import contains

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

from src.user import User

from src.farm import Farm
from src.farm_item import FarmItem
from src.farm_item import farm_items

class HomeFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)

    def init(self):
        super().init()
        self.view = sf.View()
        self.view.reset(sf.Rectangle((0, 0), (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)))
        
        self.current_item = 0 # current item in inventory list
        self.inventory_drawer = []
        for item in self.user.inventory:
            self.inventory_drawer.append(item) # so you get a basic list of each item, accessed through current_item
        
        # CONTROL WINDOW
        self.load_button = Button(sf.Vector2(16, 0), "button", self.input, "load")
        self.save_button = Button(sf.Vector2(144, 0), "button", self.input, "save")
        self.shop_button = Button(sf.Vector2(80, 32), "button", self.input, "shop")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, "lucas", self.input)
        
        self.window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), self.input)
        self.window.add_child(self.load_button)
        self.window.add_child(self.save_button)
        self.window.add_child(self.shop_button)
        self.window.add_child(self.textbox)
        
        self.gui_manager.add(self.window)
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.PacketTypes.ADD_FARM_ITEM:
            type = packet.read() # type of tree
            x = packet.read()
            y = packet.read()
            self.user.farm.add_farm_item(FarmItem(type, sf.Vector2(x, y), farm_items[type].price))

        elif packet_id == const.PacketTypes.SWITCH_FARM:
            name = packet.read()
            packet.write(const.PacketTypes.LOAD_FARM)
            packet.write(name)
            self.client.send(packet)
            if self.user.user_type == "Student":
                self.user.switch_state(const.GameStates.GUEST_FARM)
            else:
                self.user.switch_state(const.GameStates.TEACHER_GUEST_FARM)
    
    def render(self, target):
        target.view = self.view
        self.user.farm.draw(target)
        target.view = target.default_view
        
        super().render(target)
        
        # DRAW INVENTORY
        
        item = self.get_current_item()
        item = FarmItem(item, sf.Vector2(0, 0), farm_items[item].price)
        item.position = sf.Vector2(790-item.width, 0)
        item.draw(target)
        
        amnt = self.user.inventory[self.get_current_item()]
        amnt = sf.Text(str(amnt), res.font_8bit, 20)
        amnt.position = sf.Vector2(item.position.x+item.width/2, item.height/2)
        target.draw(amnt)
        
        # END

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        super().on_mouse_button_pressed(mouse_button, x, y)
        if mouse_button == sf.Mouse.LEFT:
            if self.gui_manager.point_over_any_element(x, y) is not True: # mouse isn't over window
                packet = net.Packet()
                packet.write(const.PacketTypes.ADD_FARM_ITEM)
                packet.write(self.get_current_item())
                packet.write(self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view).x)
                packet.write(self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view).y)
                self.client.send(packet)

            elif self.gui_manager.point_over_element(self.load_button, x, y) is True:
                if self.textbox.last_text is not self.user.user_name:
                    packet = net.Packet()
                    packet.write(const.PacketTypes.SWITCH_FARM)
                    packet.write(self.textbox.last_text)
                    self.client.send(packet)
                
            elif self.gui_manager.point_over_element(self.save_button, x, y) is True:
                packet = net.Packet()
                packet.write(const.PacketTypes.SAVE_FARM)
                self.user.farm.serialize(packet)
                self.client.send(packet)
                
        if mouse_button == sf.Mouse.RIGHT:
            for item in reversed(self.user.farm.farm_items):
                if contains(item.local_bounds, self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view)):
                    self.user.farm.farm_items.remove(item)
                    break # only delete one tree
                    
    def on_mouse_moved(self, pos, move):
        if self.gui_manager.point_over_any_element(pos.x, pos.y) is not True: # mouse isn't over window
            if self.mouse_state == 'down': # mouse is down
                self.view.move(-move.x, -move.y)
                
    def on_mouse_wheel_moved(self, delta, position):
        self.current_item += delta
        if self.current_item > len(self.inventory_drawer)-1:
            self.current_item = 0
            
        elif self.current_item < 0:
            self.current_item = len(self.inventory_drawer)-1
                
    def get_current_item(self):
        return self.inventory_drawer[self.current_item]
        
## GUEST FARM
        
class GuestFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)

    def init(self):
        super().init()
        self.farm = Farm()
        self.owner = User(self.client, "")
        
        # CONTROL WINDOW
        self.load_button = Button(sf.Vector2(16, 0), "button", self.input, "load")
        self.home_button = Button(sf.Vector2(144, 0), "button", self.input, "home")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, self.owner.user_name, self.input)
        
        self.window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), self.input)
        self.window.add_child(self.load_button)
        self.window.add_child(self.home_button)
        self.window.add_child(self.textbox)
        
        self.gui_manager.add(self.window)

    def handle_packet(self, packet):
        packet_id = packet.read()

        if packet_id == const.PacketTypes.LOAD_FARM: # when you first get into the state
            self.owner.deserialize(packet)
            self.farm.deserialize(packet)
            
            self.textbox.default_text = self.owner.user_name
            self.textbox.text.string = self.owner.user_name
    
    def render(self, target):
        super().render(target)
        self.farm.draw(target)

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if self.gui_manager.point_over_element(self.home_button, x, y) is True:
                self.user.switch_state(const.GameStates.HOME_FARM)
                    
            elif self.gui_manager.point_over_element(self.load_button, x, y) is True:
                if self.textbox.last_text != self.user.user_name:
                    print(self.textbox.last_text, self.user.user_name)
                    packet = net.Packet()
                    packet.write(const.PacketTypes.SWITCH_FARM)
                    packet.write(self.textbox.last_text)
                    self.client.send(packet)
                    
## TEACHER GUEST FARM STATE

class TeacherGuestFarmState(GuestFarmState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)
        
    def init(self):
        super().init()
        self.farm = Farm()
        self.owner = User(self.client, "")
        
        # CONTROL WINDOW
        self.ctrl_window = Window(sf.Vector2(260, 0), 256, 128, sf.Color(50, 50, 120, 255), self.input)
        self.add_button = Button(sf.Vector2(16, 0), "button", self.input, "add")
        self.set_button = Button(sf.Vector2(144, 0), "button", self.input, "set")
        self.points_textbox = Textbox(sf.Vector2(0, 64), 256, "amount of points", self.input)
        
        self.ctrl_window.add_child(self.add_button)
        self.ctrl_window.add_child(self.set_button)
        self.ctrl_window.add_child(self.points_textbox)
        
        self.gui_manager.add(self.ctrl_window)
        
    def handle_packet(self, packet):
        packet_id = packet.read()

        if packet_id == const.PacketTypes.LOAD_FARM: # when you first get into the state
            self.owner.deserialize(packet)
            self.farm.deserialize(packet)
            
            self.textbox.default_text = self.owner.user_name
            self.textbox.text.string = self.owner.user_name
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        super().on_mouse_button_pressed(mouse_button, x, y)
        if mouse_button == sf.Mouse.LEFT:
            if self.gui_manager.point_over_element(self.add_button, x, y) is True:
                packet = net.Packet()
                packet.write(const.PacketTypes.ADD_POINTS)
                packet.write(self.owner.user_name) # name of person
                packet.write(self.points_textbox.last_text)
                self.client.send(packet)
