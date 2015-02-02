import sfml as sf
from src.states.state import ClientState

import src.net as net
import src.const as const
import src.res as res

from src.GUI.button import Button
from src.GUI.label import Label
from src.GUI.window import Window
from src.GUI.gui_manager import GUIManager

class StatisticsState(ClientState):
	def __init__(self, client, input, gui, user):
		super().__init__(client, input, gui, user)

	def init(self):
		super().init()

		packet = net.Packet()
		packet.write(const.PacketTypes.GET_USER)
		self.client.send(packet)

		self.total_points_label = Label(sf.Vector2(16, 0), "total points:", self.input, sf.Color.WHITE)
		self.total_points_amnt = Label(sf.Vector2(144, 0), str(self.user.points), self.input, sf.Color.WHITE)

		self.close_button = Button(sf.Vector2(512-16, 0), "close", self.input, "", 1, 1, 0, 0, 0)
        
		self.window = Window(sf.Vector2(168, 50), 512, 384, sf.Color(50, 50, 120, 255), self.input)
		self.window.local_bounds.position = sf.Vector2(168, 480-self.window.height/2)
		
		self.window.add_child(self.total_points_label)
		self.window.add_child(self.total_points_amnt)

		self.window.add_child(self.close_button)

		self.gui_manager.add(self.window)

	def handle_packet(self, packet):
		packet_id = packet.read()

		if packet_id == const.PacketTypes.GET_USER:
			self.user.deserialize(packet)

	def render(self, target):
		super().render(target)

	def update(self, dt):
		super().update(dt)

	def on_mouse_button_pressed(self, mouse_button, x, y):
		super().on_mouse_button_pressed(mouse_button, x, y)

		if self.gui_manager.point_over_element(self.close_button, x, y) is True:
			self.user.switch_state(const.GameStates.HOME_FARM)