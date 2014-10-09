import sfml as sf
import src.net as net
import src.const as const

from src.users import Student
from src.users import Teacher

import re

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
    def __init__(self, server, users):
        self.server = server
        
        server.add_handler(self)
        
        self.users = users # all registered users
        self.connected_users = {}
    
    def handle_packet(self, packet, client_id):
        pass
    
    def on_connect(self, client_id):
        pass
        
    def update(self, dt):
        pass
        
    def add_points(self, packet):
        name = packet.read()
        points = packet.read()
        values = name.split()
        new_points = int(points)+int(self.users[values[0]].points)
        self.users[values[0]].points = new_points
        text = [str(new_points)]
        file = open("content/users/"+values[0]+"_"+values[1]+".txt", 'w')
        file.writelines(text)
        
    # Functions to shorten handle_packet()
    def login(self, packet, client_id):
        # Read incoming packet and save data
        f_name = packet.read()
        l_name = packet.read()
        
        user = self.users[f_name]
        user.client_id = client_id
        self.connected_users[client_id] = user
        # Send confirm login packet
        confirm_login_packet = net.Packet()
        confirm_login_packet.write(const.packet_confirm_login)
        
        with open("content/users/all_registered_users.txt") as f:
            for line in f:
                if re.match(f_name, line):
                    values = line.split()
                    if values[2] == "Student":
                        confirm_login_packet.write("Student")
                    elif values[2] == "Teacher":
                        confirm_login_packet.write("Teacher")
                        
        with open("content/users/"+f_name+"_"+l_name+".txt") as f:
            for line in f:
                values = line.split()
                user.points = values[0]
                        
        user.serialize(confirm_login_packet)
        self.server.send(client_id, confirm_login_packet)
        
    def save_student(self, packet): # only save the student, not his farm
        first_name = packet.read()
        user_type = "Student"
        points = int(self.users[first_name].points)
        l_name = self.users[first_name].last_name
        # Write data to text file
        filename = "content/users/"+first_name+"_"+l_name+".txt"
        file = open(filename, 'w')
        text = [str(points)]
        file.writelines(text)
        file.close()
                
    def save_everything(self, packet, client_id):
        # Read incoming packet
        user_type = packet.read() # student or teacher?
        student_id = packet.read()
        points = packet.read()
        f_name = packet.read()
        l_name = packet.read()
        # Write data to text file
        filename = "content/users/"+f_name+"_"+l_name+".txt"
        file = open(filename, 'w')
        text = [str(points)]
        file.writelines(text)
        file.close()
        # Get farm data
        filename = "content/farms/"+f_name+"_"+l_name+".txt"
        file = open(filename, 'w') # rewrite file everytime
        items = packet.read()
        file.write(str(items), "\n")
        for item in range(0, items):
            type = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            line = [str(type), " ", str(int(pos_x)), " ", str(int(pos_y)), "\n"]
            file.writelines(line)
        # save inventory
        inv_len = packet.read() # length of inventory
        for item in range(0, inv_len):
            
        file.close()
        