import src.net as net
import src.const as const

class Student:
    def __init__(self, id, state=None, farm=None, interface=None):
        self.client_id = id
        self.points = 0
        self.user_type = "Student"
        self.first_name = ""
        self.last_name = ""
        self.state = state # farm, shop, etc.
        self.farm = farm
        self.interface = interface
        self.inventory = {}
        self.inventory_current_item = 0

    def serialize(self, packet):
        packet.write("Student")
        packet.write(self.client_id)
        packet.write(self.points)
        packet.write(self.first_name)
        packet.write(self.last_name)

    def deserialize(self, packet):
        student = packet.read()
        self.client_id = packet.read()
        self.points = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()
        
    def switch_interface(self, interface):
        for child in self.interface.gui_manager.children:
            self.interface.gui_manager.remove(child)
        self.interface = None
        self.interface = interface

class Teacher:
    def __init__(self, id, server, state=None, farm=None, interface=None):
        self.client_id = id
        self.user_type = "Teacher"
        self.first_name = ""
        self.last_name = ""
        self.server = server
        self.state = state
        self.farm = farm
        self.interface = interface
        
    def serialize(self, packet):
        packet.write("Teacher")
        packet.write(self.client_id)
        packet.write(self.first_name)
        packet.write(self.last_name)
        packet.write(self.server)

    def deserialize(self, packet):
        teacher = packet.read()
        self.client_id = packet.read()
        self.first_name = packet.read()
        self.last_name = packet.read()
        self.server = packet.read()
        