import sfml as sf
import src.res as res
from src.rect import contains
from src.input_system import MouseHandler
from src.spritesheet import SpriteSheet

class Button():
    def __init__(self, pos, type, frames, frames_per_row, input): # assumes it's all in one picture
        self.sprite = SpriteSheet(res.textures[type])
        self.sprite.init(frames, frames_per_row)
        self.sprite.position = pos
        self.position = pos
        
        self.local_bounds = self.sprite.local_bounds
        self.local_bounds.position = pos
        
        input.add_mouse_handler(self)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        pass
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.local_bounds, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(1) # hover
        else:
            self.sprite.set_frame(0) # up
            
    def draw(self, target):
        target.draw(self.sprite)
        
    def update(self, dt):
        pass

class Window():
    def __init__(self, pos, width, height, color, input):
        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS, 4)
        self.width = width
        self.height = height
        # Set Position
        self.vertices[0].position = sf.Vector2(pos.x, pos.y)
        self.vertices[1].position = sf.Vector2(pos.x+self.width, pos.y)
        self.vertices[2].position = sf.Vector2(pos.x+self.width, pos.x+self.height)
        self.vertices[3].position = sf.Vector2(pos.x, pos.x+self.height)
        # Set Color
        for i in range(0, 4):
            self.vertices[i].color = color
        
        self.position_dirty = True # if the parent moved then this one needs to too
        self.children = []
        self.mouse_states = ['up', 'down']
        self.mouse_state = self.mouse_states[0]
        self.recalculate_position()
        
        self.input = input
        input.add_mouse_handler(self)
        
    def make_position_dirty(self):
        self.position_dirty = True
        for child in self.children:
            child.position_dirty = True
            
        self.recalculate_position()
        
    def recalculate_position(self):
        for child in self.children:
            child.sprite.position = self.vertices[0].position + child.position
            child.local_bounds.position = child.sprite.position
            child.position_dirty = False
        self.position_dirty = False
        
    def remove_child(self, element):
        self.children.remove(element)
    
    def add_child(self, element):
        self.children.append(element)
        
    def move(self, x, y):
        self.vertices[0].position += sf.Vector2(x, y)
        self.vertices[1].position += sf.Vector2(x, y)
        self.vertices[2].position += sf.Vector2(x, y)
        self.vertices[3].position += sf.Vector2(x, y)
        self.make_position_dirty();
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.mouse_state = self.mouse_states[1]
    
    def on_mouse_button_released(self, button, x, y):
        self.mouse_state = self.mouse_states[0]
    
    def on_mouse_moved(self, position, move):
        if contains(self.vertices.bounds, sf.Vector2(position.x, position.y)):
            if self.mouse_state == self.mouse_states[1]: # mouse is down
                self.move(move.x, move.y)
          
    def draw(self, target):
        target.draw(self.vertices)
        
        for child in self.children:
            child.draw(target)
            
    def update(self, dt):
        for child in self.children:
            child.update(dt)
        
