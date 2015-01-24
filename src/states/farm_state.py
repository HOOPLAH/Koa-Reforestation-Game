import sfml as sf
from src.states.state import ClientState

import src.net as net
import src.const as const
from src.rect import contains

from src.GUI.button import Button
from src.GUI.textbox import Textbox
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

from src.user import User

from src.farm_item import FarmItem
from src.farm_item import farm_items

class HomeFarmState(ClientState):
    def __init__(self, client, input, gui, user):
        super().__init__(client, input, gui, user)

    def init(self):
        super().init()
        
        # CONTROL WINDOW
        self.load_button = Button(sf.Vector2(0, 0), "button", self.input, "load")
        self.save_button = Button(sf.Vector2(0, 32), "button", self.input, "save")
        self.shop_button = Button(sf.Vector2(104, 0), "button", self.input, "shop")
        
        self.textbox = Textbox(sf.Vector2(0, 64), 256, self.user.user_name, self.input)
        
        self.ctrl_window = Window(sf.Vector2(0, 0), 256, 128, sf.Color(50, 50, 120, 255), self.input)
        self.ctrl_window.add_child(self.load_button)
        self.ctrl_window.add_child(self.save_button)
        self.ctrl_window.add_child(self.shop_button)
        self.ctrl_window.add_child(self.textbox)
        
        self.gui_manager.add(self.ctrl_window)
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.PacketTypes.ADD_FARM_ITEM:
            type = packet.read() # type of tree
            x = packet.read()
            y = packet.read()
            
            self.user.farm.add_farm_item(type, x, y)

        elif packet_id == const.PacketTypes.SWITCH_FARM:
            name = packet.read()

            self.gui_manager.remove_all()
            packet = net.Packet()
            packet.write(const.PacketTypes.LOAD_FARM)
            packet.write(name)
            self.client.send(packet)

            self.user.switch_state(const.GameStates.HOME_FARM)
    
    def render(self, target):
        super().render(target)
        
        self.user.farm.draw(target)

    def update(self, dt):
        super().update(dt)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT:
            if self.gui_manager.point_over_any_element(x, y) is not True: # mouse isn't over window
                packet = net.Packet()
                packet.write(const.PacketTypes.ADD_FARM_ITEM)
                packet.write("koa")
                packet.write(x)
                packet.write(y)
                self.client.send(packet)

            elif self.gui_manager.point_over_element(self.load_button, x, y) is True:
                packet = net.Packet()
                packet.write(const.PacketTypes.SWITCH_FARM)
                packet.write(self.textbox.last_text)
                self.client.send(packet)
        
class GuestFarmState(ClientState):
    def __init__(self, client, input, gui):
        super().__init__(client, input, gui, None)
        self.user = User(client, "")

    def init(self):
        pass

    def handle_packet(self, packet):
        packet_id = packet.read()

        if packet_id == const.PacketTypes.LOAD_FARM:
            self.user.deserialize(packet)
            print(self.user.user_name)
    
    def render(self, target):
        super().render(target)

    def update(self, dt):
        super().update(dt)
