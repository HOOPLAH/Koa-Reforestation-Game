import sfml as sf
import src.res as res
from src.rect import contains
from src.input_system import MouseHandler
from src.spritesheet import SpriteSheet

class Button:
    def __init__(self, x, y, type, frames, frames_per_row, input): # assumes it's all in one picture
        self.sprite = SpriteSheet(res.textures[type])
        self.sprite.init(frames, frames_per_row)
        self.sprite.position = sf.Vector2(x, y)
        
        self.rectangle = sf.Rectangle()
        self.rectangle.position = self.sprite.position
        self.rectangle.size = sf.Vector2(self.sprite.frame_dim.x, self.sprite.frame_dim.y)
        
        self.clicked = False
        self.clickable = True
        
        self.input = input
        input.add_mouse_handler(self)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if mouse_button == sf.Mouse.LEFT and contains(self.rectangle, sf.Vector2(x, y)) and self.clickable: # down
            self.clicked = True
            self.sprite.set_frame(2) # down
        elif self.clicked: # set it back to false
            self.clickable = False
    
    def on_mouse_button_released(self, button, x, y):
        self.clicked = False
        self.clickable = True
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.rectangle, sf.Vector2(position.x, position.y)):
            self.clicked = False
            self.clickable = True
            self.sprite.set_frame(1) # hover
        else:
            self.clicked = False
            self.clickable = True
            self.sprite.set_frame(0) # up
    