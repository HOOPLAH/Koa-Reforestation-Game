import sfml as sf
import src.net as net
import src.res as res

class FarmItem: # something placeable on the farm (ex. trees)
    def __init__(self, type, pos, price):
        self.type = type
        self.sprite = sf.Sprite(res.textures[type])
        self.sprite.position = pos 
        self.local_bounds = sf.Rectangle(pos, sf.Vector2(self.sprite.texture.width, self.sprite.texture.height))
        self.position = pos
        self.price = price # how much it costs to buy
        
    def serialize(self, packet):
        packet.write(self.type)
        packet.write(self.position.x)
        packet.write(self.position.y)
        
    def deserialize(self, packet):
        self.type = packet.read()
        self.position.x = packet.read()
        self.position.y = packet.read()
        
    def draw(self, target):
        self.sprite.position = self.position
        target.draw(self.sprite)
        
# farm land items
farm_items = {}
farm_items["koa"] = FarmItem("koa", sf.Vector2(0, 0), 5)
farm_items["pine"] = FarmItem("pine", sf.Vector2(0, 0), 10)