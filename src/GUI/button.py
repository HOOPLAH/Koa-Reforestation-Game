import sfml as sf
from src.GUI.element import SpriteElement
from src.GUI.label import Label

from src.rect import contains

class Button(SpriteElement):
    def __init__(self, pos, type, input, text=None): # assumes it's all in one picture
        super().__init__(pos, type, 3, 3, input)
        
        self.label = Label(pos, text, input)
        self.text_bounds = self.label.text.local_bounds
        self.text_offset = self.center - sf.Vector2(self.text_bounds.width/2, self.text_bounds.height/1.5)
        self.add_child(self.label)
        
    def on_mouse_button_pressed(self, mouse_button, x, y):
        if contains(self.local_bounds, sf.Vector2(x, y)):
            self.sprite.set_frame(2) # down
    
    def on_mouse_button_released(self, button, x, y):
        self.sprite.set_frame(0) # up
            
    def on_mouse_moved(self, position, move):
        if contains(self.local_bounds, sf.Vector2(position.x, position.y)):
            self.sprite.set_frame(1) # hover
        else:
            self.sprite.set_frame(0) # up
            
    def update(self, dt):
        super().update(dt)
        self.label.text.position = self.sprite.position + self.text_offset
            
    def draw(self, target):
        super().draw(target)
        self.label.draw(target)
