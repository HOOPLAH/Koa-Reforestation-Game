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

from src.farm_item import FarmItem
from src.farm_item import farm_items

# FarmInterface draws all the buttons and the farm currently on-screen
class FarmInterface(Interface):
    def __init__(self, client, student, farm, input):
        super().__init__(client, student, input)

        # CONTROL WINDOW
        self.load_button = Button(sf.Vector2(0, 0), "button", input, "load")
        self.save_button = Button(sf.Vector2(0, 32), "button", input, "save")
        self.shop_button = Button(sf.Vector2(104, 0), "button", input, "shop")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, student.first_name+" "+student.last_name, input)
        
        self.ctrl_window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), input)
        self.ctrl_window.add_child(self.load_button)
        self.ctrl_window.add_child(self.save_button)
        self.ctrl_window.add_child(self.shop_button)
        self.ctrl_window.add_child(self.textbox)
        
        # SHOP WINDOW
        self.koa_shop_button = Button(sf.Vector2(0, 0), "button", input, "koa")
        self.pine_shop_button = Button(sf.Vector2(0, 32), "button", input, "pine")
        
        self.shop_window = Window(sf.Vector2(168, 50), 512, 384, sf.Color(50, 50, 120, 255), input)
        self.shop_window.local_bounds.position = sf.Vector2(168, 480-self.shop_window.height/2)
        self.shop_window.add_child(self.koa_shop_button)
        self.shop_window.add_child(self.pine_shop_button)
        self.shop_open = False
        
        self.gui_manager.add(self.ctrl_window)
        
        self.current_farm = farm # The farm we're currently drawing
        self.owner_name = student.first_name+" "+student.last_name
        
        self.inventory_to_draw = []
        self.current_inv_item = 0
        for item in self.user.inventory:
            self.inventory_to_draw.append(item)
        
    # MOUSE
    def on_mouse_button_released(self, mouse_button, x, y):
        super().on_mouse_button_released(mouse_button, x, y)
        
        if self.owner_name == self.textbox.last_text: # on own farm
            if mouse_button == sf.Mouse.LEFT:
                if not self.mouse_over_window(x, y):
                    if len(self.inventory_to_draw) > 0 and self.shop_open == False:
                        packet = net.Packet()
                        packet.write(const.packet_request_place_item)
                        packet.write(self.inventory_to_draw[self.current_inv_item])
                        packet.write(self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view).x)
                        packet.write(self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view).y)
        
                        self.client.send(packet)

                    if self.shop_open == True:
                        self.gui_manager.remove(self.shop_window)
                        self.shop_open = False
                        
            if mouse_button == sf.Mouse.RIGHT:
                for item in reversed(self.current_farm.land_items):
                    if contains(item.local_bounds, self.input.window.map_pixel_to_coords(sf.Vector2(x, y), self.view)):
                        self.current_farm.land_items.remove(item)
                        break # only delete one tree
                    
            if contains(self.save_button.local_bounds, sf.Vector2(x, y)):
                # Save user information
                packet = net.Packet()
                packet.write(const.packet_save_everything)
                self.user.serialize(packet)

                # Save farm information
                packet.write(len(self.current_farm.land_items))
                for item in self.current_farm.land_items:
                    item.serialize(packet)
                # Send file
                self.client.send(packet)

            if contains(self.shop_button.local_bounds, sf.Vector2(x, y)):
                self.shop_open = True
                self.gui_manager.add(self.shop_window)

            if self.shop_open:
                if contains(self.koa_shop_button.local_bounds, sf.Vector2(x, y)):
                    packet = net.Packet()
                    packet.write(const.packet_request_add_inventory)
                    packet.write("koa")
                    self.client.send(packet)
                elif contains(self.pine_shop_button.local_bounds, sf.Vector2(x, y)):
                    packet = net.Packet()
                    packet.write(const.packet_request_add_inventory)
                    packet.write("pine")
                    self.client.send(packet)
                    
        if contains(self.load_button.local_bounds, sf.Vector2(x, y)):
            packet = net.Packet()
            packet.write(const.packet_request_load_farm)
            packet.write(self.textbox.text.string) # send the name 
            self.client.send(packet)
                
    def on_mouse_moved(self, position, move):
        if not self.mouse_over_window(position.x, position.y):
            if self.mouse_state == 'down': # mouse is down
                self.view.move(-move.x, -move.y)
                
    def on_mouse_wheel_moved(self, delta, position):
        self.current_inv_item += delta
        if self.current_inv_item > len(self.inventory_to_draw)-1:
            self.current_inv_item = 0
        elif self.current_inv_item < 0:
            self.current_inv_item = len(self.inventory_to_draw)-1
            
    def draw(self, target):
        target.view = self.view
        
        for item in self.current_farm.land_items:
            item.draw(target)
            
        target.view = target.default_view
        
        points = sf.Text(str(self.user.points), res.font_8bit, 20)
        points.position = sf.Vector2(800 - points.local_bounds.width, 0)
        target.draw(points)
        
        if len(self.user.inventory) > 0:
            item = self.inventory_to_draw[self.current_inv_item]
            item = FarmItem(item, sf.Vector2(0, 0), farm_items[item].price)
            item.position = sf.Vector2(790-item.width, 0)
            item.draw(target)

            amnt = self.user.inventory[self.inventory_to_draw\
                                       [self.current_inv_item]]
            amnt = sf.Text(str(amnt), res.font_8bit, 20)
            amnt.position = sf.Vector2(item.position.x+item.width/2, item.height/2)
            target.draw(amnt)

            if self.user.inventory[self.inventory_to_draw[self.current_inv_item]] == 0:
                self.current_inv_item = int(self.current_inv_item)-1
                del self.user.inventory[self.inventory_to_draw[self.current_inv_item+1]]
                del self.inventory_to_draw[self.current_inv_item+1]
                    
        super().draw(target)
