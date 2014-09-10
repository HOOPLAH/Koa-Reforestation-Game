import sfml as sf
import src.res as res
from src.rect import contains
from src.GUI.label import Label
from src.GUI.gui_manager import GUIManager

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class Interface:
    def __init__(self, client, user, input):
        self.client = client
        self.user = user
        self.gui_manager = GUIManager()
        self.input = input
        input.add_key_handler(self)
        input.add_text_handler(self)
        input.add_mouse_handler(self)
        
        self.points = Label(sf.Vector2(0, 0), "", input)
        if self.user and self.user.user_type is "Student":
            self.points.text.string = str(self.user.points)
            self.points.local_bounds.position.x = 800-self.points.local_bounds.width
            
        self.gui_manager.add(self.points)
        
        self.view = sf.View()
        self.view.reset(sf.Rectangle((0, 0), (800, 480)))
        self.converted_coords = sf.Vector2(0, 0)
        
        self.mouse_state = 'up'
        
    def mouse_over_window(self, x, y): # Hack 
        for i in range(0, len(self.gui_manager.children)):
            if contains(self.gui_manager.children[i].local_bounds, sf.Vector2(x, y)):
                return True
            else:
                continue
            
        return False
        
    # KEYBOARD
    def on_key_pressed(self, key_code):
        pass
    
    def on_key_released(self, key_code):
        pass
        
    # TEXT
    def on_text_entered(self, unicode):
        pass
        
    # MOUSE
    def on_mouse_button_pressed(self, mouse_button, x, y):
        self.mouse_state = 'down'
    
    def on_mouse_button_released(self, button, x, y):
        self.mouse_state = 'up'
            
    def on_mouse_moved(self, position, move):
        pass
        
    def update(self, dt):
        self.gui_manager.update(dt)
        
    def draw(self, target):
        self.gui_manager.draw(target)