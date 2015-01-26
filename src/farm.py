import sfml as sf

from src.farm_item import farm_items
from src.farm_item import FarmItem

class Farm:
	def __init__(self):
		self.farm_items = []

	def add_farm_item(self, type, x, y):
		self.farm_items.append(FarmItem(type, sf.Vector2(x, y), farm_items[type].price))
		
	def remove_all(self):
	    self.farm_items = []

	def serialize(self, packet):
		packet.write(len(self.farm_items))
		for item in self.farm_items:
			item.serialize(packet)

	def deserialize(self, packet):
		size = packet.read()
		for i in range(0, size):
			item = FarmItem("koa", sf.Vector2(0, 0), 0)
			item.deserialize(packet)
			self.farm_items.append(item)

	def draw(self, target):
		for item in self.farm_items:
			item.draw(target)
