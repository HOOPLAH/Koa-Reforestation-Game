import sfml as sf
from src.GUI.element import SpriteElement
from src.GUI.label import Label

from src.rect import contains

class Button(SpriteElement):
    def __init__(self, pos, type, input, text=None, frames=3, frames_per_row=3, up=0, hover=1, down=2): # assumes it's all in one picture
        super().__init__(pos, type, input, frames, frames_per_row)
        
        self.label = Label(pos, text, input)
        self.text_bounds = self.label.text.local_bounds
        self.text_offset = self.center - sf.Vector2(self.text_bounds.width/2, self.text_bounds.height/1.5)
        self.add_child(self.label)

        self.up = up
        self.hover = hover
        self.down = down
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if contains(self.local_bounds, sf.Vector2(x, y)):
            self.sprite.set_frame(self.down) # down
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(self.up) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.local_bounds, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(self.hover) # hover
        else:
            self.sprite.set_frame(self.up) # up
            
    def update(self, dt):
        super().update(dt)
        self.label.text.position = self.sprite.position + self.text_offset
            
    def draw(self, target):
        super().draw(target)
        self.label.draw(target)
