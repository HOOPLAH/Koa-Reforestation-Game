class Interface:
    def __init__(self, client, student, input):
        self.client = client
        self.student = student
        input.add_key_handler(self)
        input.add_text_handler(self)
        input.add_mouse_handler(self)
        
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
        pass
            
    def on_mouse_button_released(self, button, x, y):
        pass
            
    def on_mouse_moved(self, position, move):
        pass
        
    def update(self, dt):
        pass
        
    def draw(self, target):
        points = sf.Text("0", res.font_8bit, 20)
        points.position = sf.Vector2(760, 0)
        points.string = str(self.student.points)
        target.draw(points)
