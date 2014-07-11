import src.net as net
import src.const as const
from src.student import Student

class Teacher:
    def __init__(self, server):
        self.server = server # Teacher is admin, knows of server!
        
    def set_student_points(self, student, points):
        student.points = points
        packet = net.Packet()
        packet.write(const.packet_add_points)
        packet.write(student.points)
        self.server.send(student.id, packet)
        
    def add_to_student_points(self, student, points):
        student.points += points
        packet = net.Packet()
        packet.write(const.packet_add_points)
        packet.write(student.points)
        self.server.send(student.id, packet)
        
    def register_student(self, student):
        pass
    