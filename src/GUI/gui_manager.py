import sfml as sf
from src.rect import contains
        
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
        
    def point_over_any_element(self, x, y):
        for i in range(0, len(children)):
            if contains(children[i].local_bounds, sf.Vector2(x, y)):
                return True
            
        return False
        
    def point_over_element(self, element, x, y):
        if self.exists(element):
            for child in self.children:
                if child == element:
                    if contains(child.local_bounds, sf.Vector2(x, y)):
                        return True
        
        return False
    
    def update(self, dt):
        for child in self.children:
            child.update(dt)
    
    def draw(self, target):
        for child in self.children:
            child.draw(target)
        
