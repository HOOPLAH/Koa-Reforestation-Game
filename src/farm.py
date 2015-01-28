import sfml as sf

from src.farm_item import farm_items
from src.farm_item import FarmItem

class Farm:
    def __init__(self):
        self.farm_items = []

    def add_farm_item(self, item):
        self.farm_items.append(item)
        
    def remove(self, item):
        self.farm_items.remove(item)
		
    def remove_all(self):
        self.farm_items = []

    def serialize(self, packet):
        packet.write(len(self.farm_items))
        for item in self.farm_items:
            item.serialize(packet)

    def deserialize(self, packet):
        size = packet.read()
        for i in range(0, size):
            type = packet.read()
            price = packet.read()
            x = packet.read()
            y = packet.read()
            
            item = FarmItem(type, sf.Vector2(x, y), price)
            self.farm_items.append(item)

    def draw(self, target):
        for item in self.farm_items:
            item.draw(target)
