import sfml as sf
import re
import src.net as net
import src.const as const

from src.user import User

from src.farm_item import farm_items
from src.farm_item import FarmItem
from src.farm import Farm
        
class ServerPacketManager:
    def __init__(self, server):
        self.server = server
        self.server.add_handler(self)
        
        self.users = {} # called by username, any user who is registered
        self.connected_users = {} # called by client_id
        
        self.register_students()
        
    def on_connect(self, client_id):
        pass
        
    def on_disconnect(self, client_id):
        del self.connected_users[client_id] # delete that one user from the list
        
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()
    
        if packet_id == const.PacketTypes.LOGIN:
            self.on_login(packet, client_id)
            
        elif packet_id == const.PacketTypes.ADD_FARM_ITEM:
            type = packet.read() # type of tree
            x = packet.read()
            y = packet.read()
            
            # got all data from packet, send it back with new data
            packet.write(packet_id)
            packet.write(type)
            packet.write(x)
            packet.write(y)
            self.send(client_id, packet)

        elif packet_id == const.PacketTypes.SWITCH_FARM:
            name = packet.read()

            # got all data from packet, send it back with new data
            if name in self.users:
                packet = net.Packet()
                packet.write(packet_id)
                packet.write(name)
                self.send(client_id, packet)

        elif packet_id == const.PacketTypes.LOAD_FARM:
            name = packet.read()

            # got all data from packet, send it back with new data
            packet.write(packet_id)
            self.load_farm(self.users[name])
            self.users[name].farm.serialize(packet)
            self.send(client_id, packet)
            
        elif packet_id == const.PacketTypes.SAVE_FARM:
            farm = Farm()
            farm.deserialize(packet)
            user = self.connected_users[client_id]
            file = open("content/farms/"+user.first_name+"_"+user.last_name+".txt", "w+")
            for item in farm.farm_items:
                line = [str(item.type), " ", str(int(item.position.x)), " ", str(int(item.position.y)), "\n"]
                file.writelines(line)
                
            file.close()
        
    def send(self, client_id, packet):
        self.server.send(client_id, packet)
        
    def broadcast(self, packet):
        self.server.broadcast(packet)
        
    # FN TO SHORTEN CODE ABOVE -- WARNING: MESSY #
    #                                            #
    #                                            #
    # FN TO SHORTEN CODE ABOVE -- WARNING: MESSY #
    
    # --
    # REGISTER STUDENTS
    # --
    
    def register_students(self):
        filename = "content/users/all_registered_users.txt"
        file = open(filename, 'r')
        for line in file:
            user = User(None, "")
            values = line.split() # each word(value) in txt file
            # create new student, add him to users list
            user.user_type = values[0]
            user.first_name = values[1]
            user.last_name = values[2]
            user.user_name = values[3]
            user.password = values[4]
            
            # get user data (points, inventory, farm)
            self.load_user_data(user)
            self.load_farm(user)
            
            self.users[user.user_name] = user

    # --
    # LOGIN
    # --
    
    def on_login(self, packet, client_id):
        # read incoming packet and save data
        username = packet.read()
        password = packet.read()
        
        # get user from registered users
        if self.users[username].password:
            user = self.users[username]
            user.client_id = client_id
            self.connected_users[client_id] = user
            
            # get user info
            with open("content/users/all_registered_users.txt") as file:
                for line in file:
                    if re.match(username, line):
                        pass # don't need it right now
            
            # Send new packet
            new_packet = net.Packet()
            new_packet.write(const.PacketTypes.LOGIN)                
            user.serialize(new_packet)
            self.send(client_id, new_packet)
            
    def load_user_data(self, user):
        with open("content/users/"+user.first_name+"_"+user.last_name+".txt") as file:
            user.points = file.readline()
            
            inventory_size = file.readline() # make sure this is the last bit of data in file
            for line in file:
                values = line.split()
                type = values[0]
                amount = values[1]
                user.inventory[type] = amount
            
    def load_farm(self, user):
        user.farm.remove_all()
        with open("content/farms/"+user.first_name+"_"+user.last_name+".txt") as file:
            for line in file:
                values = line.split()
                user.farm.add_farm_item(values[0], float(values[1]), float(values[2]))
