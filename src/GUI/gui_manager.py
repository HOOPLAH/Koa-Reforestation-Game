import sfml as sf
from src.rect import contains
from src.input_system import MouseHandler
        
class GUIManager():
    def __init__(self):
        self.children = []
        
    def add(self, element):
        self.children.append(element)
        
    def remove(self, element):
        self.children.remove(element)
        
    def remove_all(self):
        self.children = []
        
    def exists(self, element): 
        for child in self.children:
            if child == element:
                return True
                
        return False
    
    def update(self, dt):
        for child in self.children:
            child.update(dt)
    
    def draw(self, target):
        for child in self.children:
            child.draw(target)
        
