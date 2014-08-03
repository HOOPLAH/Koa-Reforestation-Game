import sfml as sf
import src.net as net
import src.res as res

class FarmLandItem: # something placeable on the farm (ex. trees)
    def __init__(self, type, pos):
        self.type = type
        self.sprite = sf.Sprite(res.textures[type])
        self.sprite.position = pos 
        self.local_bounds = sf.Rectangle(pos, sf.Vector2(self.sprite.texture.width, self.sprite.texture.height))
        self.position = pos
        
    def serialize(self, packet):
        packet.write(self.type)
        packet.write(self.position.x)
        packet.write(self.position.y)
        
    def deserialize(self, packet):
        self.type = packet.read()
        self.position.x = packet.read()
        self.position.y = packet.read()
        
    def draw(self, target):
        target.draw(self.sprite)