from src.states.state import GameStates

class User:
    def __init__(self, client, user_type):
        if client is not None:
            self.client = client
        self.user_type = user_type
	        
        self.first_name = ""
        self.last_name = ""
        self.user_name = ""
        self.password = ""
		
        self.points = 0
        self.farm = None
        self.inventory = {}
		
        self.states = []
        self.state = None
		
    def serialize(self, packet):
        packet.write(self.user_type)
        packet.write(self.first_name)
        packet.write(self.last_name)
        packet.write(self.user_name)
        packet.write(self.password)
        packet.write(self.points)
        
        packet.write(len(self.inventory))
        for item in self.inventory:
            packet.write(item) # type
            packet.write(self.inventory[item]) # amount
		
    def deserialize(self, packet):
        self.user_type = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()
        self.user_name = packet.read()
        self.password = packet.read()
        self.points = packet.read()
        
        inventory_size = packet.read()
        for item in range(0, inventory_size):
            type = packet.read()
            amount = packet.read()
            self.inventory[type] = amount
            
        print(self.inventory["koa"])
		
    def render(self, target):
        self.states[self.state].render(target)
		
    def update(self, dt):
        self.states[self.state].update(dt)
