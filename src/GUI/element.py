import sfml as sf
import src.res as res
from src.spritesheet import SpriteSheet

class Element:
    def __init__(self, pos, input):
        self.position = pos # position on gui window (not sfml window)
        self.position_dirty = True
        self.local_bounds = sf.Rectangle(pos, sf.Vector2(0, 0))
        
        self.children = []
        self.parent = None
        
        input.add_key_handler(self)
        input.add_mouse_handler(self)
        
    def add_child(self, element):
        self.children.append(element)
        
    def remove_child(self, element):
        self.children.remove(element)
        
    def on_key_pressed(self, key_code):
        pass
    
    def on_key_released(self, key_code):
        pass
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        pass
    
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass
        
    def on_mouse_wheel_moved(self, delta, position):
        pass
        
    def update(self, dt):
        pass
            
    def draw(self, target):
        pass

class SpriteElement(Element):
    def __init__(self, pos, type, input, frames, frames_per_row):
        super().__init__(pos, input)
        self.sprite = SpriteSheet(res.textures[type])
        self.sprite.init(frames, frames_per_row)
        self.sprite.position = pos
        self.local_bounds = self.sprite.local_bounds
        self.center = sf.Vector2(self.local_bounds.width/2, self.local_bounds.height/2)
        
    def update(self, dt):
        self.sprite.position = self.local_bounds.position
        
    def draw(self, target):
        target.draw(self.sprite)
