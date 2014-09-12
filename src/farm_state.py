import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.state import StateClient
from src.state import StateServer

from src.users import Student
from src.farm_item import FarmItem
from src.farm_interface import FarmInterface

# FarmClient is the client's farm, FarmInterface is the farm on the screen
class ClientFarmState(StateClient):
    def __init__(self, client, student, input):
        super().__init__(client, student, input)
        
        self.land_items = []
        
    def handle_packet(self, packet):
        super().handle_packet(packet)
        packet_id = packet.read()
        if packet_id == const.packet_place_item:
            self.place_item(packet, self.land_items)
        elif packet_id == const.packet_load_farm:
            self.land_items[:] = [] # empty land_items[]
            self.load_farm(packet, self.land_items)
    
    # Functions to shorten handle_packet()
    def place_item(self, packet, land_items):
        item_id = packet.read()
        pos_x = packet.read()
        pos_y = packet.read()
        item = FarmItem(item_id, sf.Vector2(pos_x, pos_y))
        land_items.append(item)
        
    def load_farm(self, packet, land_items):
        num_of_trees = packet.read()
        for tree in range(0, int(num_of_trees)):
            item_id = packet.read()
            pos_x = int(packet.read())
            pos_y = int(packet.read())
            item = FarmItem(item_id, sf.Vector2(pos_x, pos_y))
            self.land_items.append(item)
            
# FarmServer controls all the farms
class ServerFarmState(StateServer):
    def __init__(self, server, users):
        super().__init__(server, users)
        
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()
        
        if packet_id == const.packet_login:
            self.login(packet, client_id)
        elif packet_id == const.packet_save_student:
            self.save_student(packet)
        elif packet_id == const.packet_save_everything:
            self.save_everything(packet, client_id)
        elif packet_id == const.packet_request_place_item:
            self.on_request_place_item(packet, client_id)
        elif packet_id == const.packet_request_load_farm:
            self.on_request_load_farm(packet, client_id)
        elif packet_id == const.packet_add_points:
            self.add_points(packet)
    
    # Functions to shorten handle_packet()
    def on_request_place_item(self, packet, client_id):
        # Read incoming packet
        item_packet = net.Packet()
        item_id = packet.read()
        pos_x = packet.read()
        pos_y = packet.read()
        # Write new one to send to client to place tree
        item_packet.write(const.packet_place_item)
        item_packet.write(item_id)
        item_packet.write(pos_x)
        item_packet.write(pos_y)
        self.server.send(client_id, item_packet)
        
    def on_request_load_farm(self, packet, client_id):
        name = packet.read()
        name = name.split() # student whose farm we're trying to load
        student = self.connected_users[client_id] # student who sent packet
        filename = "content/farms/"+name[0]+"_"+name[1]+".txt"
        with open(filename, 'r') as f:
            lines = f.readlines()
            num_of_trees = len([l for l in lines if l.strip(' \n') != ''])
            farm_packet = net.Packet()
            farm_packet.write(const.packet_load_farm)
            farm_packet.write(num_of_trees)
            with open(filename) as file:
                for line in file:
                    values = line.split()
                    farm_packet.write(values[0])
                    farm_packet.write(values[1])
                    farm_packet.write(values[2])
            self.server.send(client_id, farm_packet)