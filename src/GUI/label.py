import sfml as sf
from src.GUI.element import Element
import src.res as res

class Label(Element):
    def __init__(self, pos, text, input, color=None):
        super().__init__(pos, input)
        self.text = sf.Text(text, res.font_farmville, 20)
        self.text.color = sf.Color.BLACK
        if color:
            self.text.color = color
        self.local_bounds = self.text.local_bounds
        
    def update(self, dt):
        self.text.position = self.local_bounds.position
        
    def draw(self, target):
        target.draw(self.text)