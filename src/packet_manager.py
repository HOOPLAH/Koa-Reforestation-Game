import re
import src.net as net
import src.const as const

from src.user import User
        
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
        pass
        
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()
    
        if packet_id == const.PacketTypes.LOGIN:
            self.on_login(packet, client_id)
        
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
            values = line.split() # each word(value) in txt file
            # create new student, add him to users list
            # client, server, states, user_type
            self.users[values[3]] = User(None, values[0]) # empty student, found by username
            self.users[values[3]].first_name = values[1]
            self.users[values[3]].last_name = values[2]
            self.users[values[3]].username = values[3]
            self.users[values[3]].password = values[4]

    # --
    # LOGIN
    # --
    
    def on_login(self, packet, client_id):
        # read incoming packet and save data
        username = packet.read()
        pw = packet.read()
        
        # get user from registered users
        user = self.users[username]
        user.client_id = client_id
        self.connected_users[client_id] = user
        
        # get user info
        with open("content/users/all_registered_users.txt") as file:
            for line in file:
                if re.match(username, line):
                    pass # don't need it right now
                        
        # get user data (points, inventory)              
        with open("content/users/"+user.first_name+"_"+user.last_name+".txt") as file:
            user.points = file.readline()
            
            inventory_size = file.readline() # make sure this is the last bit of data in file
            for line in file:
                values = line.split()
                type = values[0]
                amount = values[1]
                user.inventory[type] = amount
        
        # Send new packet
        new_packet = net.Packet()
        new_packet.write(const.PacketTypes.LOGIN)                
        user.serialize(new_packet)
        self.send(client_id, new_packet)
