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

class ShopState(ClientState):
	def __init__(self, client, input, gui, user):
		super().__init__(client, input, gui, user)

	def init(self):
		super().init()

		self.koa_button = Button(sf.Vector2(16, 0), "koa", self.input, "", 1, 1, 0, 0, 0)
		self.iliahi_button = Button(sf.Vector2(144, 0), "iliahi", self.input, "", 1, 1, 0, 0, 0)
		self.close_button = Button(sf.Vector2(512-16, 0), "close", self.input, "", 1, 1, 0, 0, 0)
        
		self.window = Window(sf.Vector2(168, 50), 512, 384, sf.Color(50, 50, 120, 255), self.input)
		#self.window = Window(sf.Vector2(0, 0), 512, 384, sf.Color(50, 50, 120, 255), self.input)
		self.window.local_bounds.position = sf.Vector2(168, 480-self.window.height/2)
		self.window.add_child(self.koa_button)
		self.window.add_child(self.iliahi_button)
		self.window.add_child(self.close_button)

		self.gui_manager.add(self.window)

	def handle_packet(self, packet):
		packet_id = packet.read()

		if packet_id == const.PacketTypes.ADD_INVENTORY_ITEM:
			self.user.deserialize(packet)

	def render(self, target):
		super().render(target)

	def update(self, dt):
		super().update(dt)

	def on_mouse_button_pressed(self, mouse_button, x, y):
		super().on_mouse_button_pressed(mouse_button, x, y)

		if self.gui_manager.point_over_element(self.close_button, x, y) is True:
			self.user.switch_state(const.GameStates.HOME_FARM)

		if self.gui_manager.point_over_element(self.koa_button, x, y) is True:
			packet = net.Packet()
			packet.write(const.PacketTypes.ADD_INVENTORY_ITEM)
			packet.write("koa")
			self.client.send(packet)

		elif self.gui_manager.point_over_element(self.iliahi_button, x, y) is True:
			packet = net.Packet()
			packet.write(const.PacketTypes.ADD_INVENTORY_ITEM)
			packet.write("iliahi")
			self.client.send(packet)