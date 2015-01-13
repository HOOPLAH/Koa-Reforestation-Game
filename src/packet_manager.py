import src.net as net
import src.const as const

from src.user import User

class ClientPacketManager:
    def __init__(self, user):
        self.user = user
        self.client = user.client
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.PacketTypes.LOGIN:
            self.user.deserialize(packet)
            
    def send(self, packet):
        self.client.send(packet)
        
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
            if values[0] == "Student":
                # create new student, add him to users list
                # client, server, states, user_type
                self.users[values[2]] = User(None, None, "Student") # empty student, found by username
                self.users[values[2]].first_name = values[0] # values[2] is username
                self.users[values[2]].last_name = values[1]
                
                # get points from different file
                self.data_file = open("content/users/"+values[0]+"_"+values[1]+".txt", 'r')
                for data_line in data_file:
                    data_values = data_line.split()
                    self.users[values[0]].points = data_values[0]
                    
            elif values[0] == "Teacher":
                # create new teacher, add him to users list
                # client, server, states, user_type
                self.users[values[0]] = User(None, self.server, "Teacher") # empty teacher
                self.users[values[0]].first_name = values[0] # values[0] is first name
                self.users[values[0]].last_name = values[1]
                
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
                    values = line.split()
                    user.user_type = values[0] # student or teacher
                        
        # get user info - continued                
        with open("content/users/"+user.first_name+"_"+user.last_name+".txt") as file:
            user.points = file.readline()
            
        # load student inventory  
        with open("content/inventories/"+user.first_name+"_"+user.last_name+".txt") as file:
            inventory_size = file.readline()
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
