import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.users import Student
from src.users import Teacher
from src.farm_interface import FarmInterface

import os

class FarmLandItem: # something placeable on the farm (ex. trees)
    def __init__(self, type, pos):
        self.type = type
        self.sprite = sf.Sprite(res.textures[type])
        self.sprite.position = pos
        self.position = pos
        
    def serialize(self, packet):
        packet.write(self.type)
        packet.write(self.position.x)
        packet.write(self.position.y)
        
    def deserialize(self, packet):
        self.type = packet.read()
        self.position.x = packet.read()
        self.position.y = packet.read()
        
    def draw(self, target):
        target.draw(self.sprite)

# FarmClient is the client's farm, FarmInterface is the farm on the screen
class FarmClient:
    def __init__(self, client, student, input):
        self.input = input
        self.client = client
        self.student = student # the owner of the farm
        
        client.add_handler(self)
        
        self.land_items = []
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.packet_add_points:
            self.student_owner.points = packet.read()
        elif packet_id == const.packet_place_item:
            item_id = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            item = FarmLandItem(item_id, sf.Vector2(pos_x, pos_y))
            self.land_items.append(item)
        elif packet_id == const.packet_load_farm:
            num_of_trees = packet.read()
            for tree in range(0, int(num_of_trees)):
                item_id = packet.read()
                pos_x = int(packet.read())
                pos_y = int(packet.read())
                item = FarmLandItem(item_id, sf.Vector2(pos_x, pos_y))
                self.land_items.append(item)
            
    def update(self, dt):
        self.input.handle()
        self.student.interface.update(dt)
        
    def draw(self, target):
        self.student.interface.draw(target)
            
# FarmServer controls all the farms
class FarmServer:
    def __init__(self, server):
        self.server = server
        
        server.add_handler(self)
        
        self.users = {}
        
    def handle_packet(self, packet, client_id):
        packet_id = packet.read()
        
        if packet_id == const.packet_login:
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
                            new_student = Student(client_id, None, None)
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
        elif packet_id == const.packet_save:
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
        elif packet_id == const.packet_request_place_item:
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
        elif packet_id == const.packet_request_load_farm:
            farm_owner_id = packet.read()
            student = self.users[farm_owner_id]
            filename = "content/farms/"+student.first_name+"_"+student.last_name+".txt"
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
            
    def on_connect(self, client_id):
        pass
        
    def update(self, dt):
        pass
    