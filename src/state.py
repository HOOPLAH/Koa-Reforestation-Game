import sfml as sf
import src.net as net
import src.const as const

from src.users import Student
from src.users import Teacher
from src.farm_land_item import FarmLandItem

import os

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
        
    # Functions to shorten handle_packet()
    def add_points(self, packet):
        self.student.points = packet.read()
        
class StateServer:
    def __init__(self, server):
        self.server = server
        
        server.add_handler(self)
        
        self.users = {}
    
    def handle_packet(self, packet, client_id):
        pass
    
    def on_connect(self, client_id):
        pass
        
    def update(self, dt):
        pass
    
    # Functions to shorten handle_packet()
    def login(self, packet, client_id):
        # Read incoming packet and save data
        first_name = packet.read()
        last_name = packet.read()
        # Check if user exists already
        filename = "content/users/"+first_name+"_"+last_name+".txt"
        if os.path.isfile(filename): # file exists so user exists
            with open(filename) as file:
                for line in file:
                    values = line.split()
                    if values[2] == "Student":
                        new_student = Student(client_id)
                        new_student.first_name = first_name
                        new_student.last_name = last_name
                        new_student.points = values[3]
                        self.users[client_id] = new_student
                        # Send confirm login packet
                        confirm_login_packet = net.Packet()
                        confirm_login_packet.write(const.packet_confirm_login)
                        confirm_login_packet.write("Student")
                        new_student.serialize(confirm_login_packet)
                        self.server.send(client_id, confirm_login_packet)
                    elif values[2] == "Teacher":
                        new_teacher = Teacher(client_id, self.server)
                        new_teacher.first_name = first_name
                        new_teacher.last_name = last_name
                        self.users[client_id] = new_teacher
                        # Send confirm login packet
                        confirm_login_packet = net.Packet()
                        confirm_login_packet.write(const.packet_confirm_login)
                        confirm_login_packet.write("Teacher")
                        self.users[new_teacher.client_id].serialize(confirm_login_packet)
                        self.server.send(client_id, confirm_login_packet)
        else:
            message = "User \'"+self.users[client_id].first_name+" "+self.users[client_id].last_name+"\' doesn't exist"
            # Send deny login packet
            deny_login_packet = net.Packet()
            deny_login_packet.write(const.packet_deny_login)
            deny_login_packet.write(message)
            self.server.send(client_id, deny_login_packet)
            
    def save(self, packet, client_id):
        # Read incoming packet
        save_packet = net.Packet()
        user_type = packet.read() # student or teacher?
        student_id = packet.read()
        points = packet.read()
        f_name = packet.read()
        l_name = packet.read()
        # Write data to text file
        filename = "content/users/"+f_name+"_"+l_name+".txt"
        file = open(filename, 'w')
        text = [f_name, " ", l_name, " ", user_type, " ", str(points)]
        file.writelines(text)
        file.close()
        # Get farm data
        filename = "content/farms/"+f_name+"_"+l_name+".txt"
        file = open(filename, 'w') # rewrite file everytime
        items = packet.read()
        for item in range(0, items):
            type = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            line = [str(type), " ", str(pos_x), " ", str(pos_y), "\n"]
            file.writelines(line)
        file.close()