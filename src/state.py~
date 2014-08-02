import src.net as net
import src.const as const

class StateClient:
    def __init__(self, client, student, input):
        self.client = client
        self.student = student # the owner of the farm
        self.input = input
        
        client.add_handler(self)
        
    def handle_packet(self, packet):
        pass
        
    def update(self, dt):
        self.input.handle()
        self.student.interface.update(dt)
        
    def draw(self, target):
        self.student.interface.draw(target)
        
class StateServer:
    def __init__(self):
        pass
