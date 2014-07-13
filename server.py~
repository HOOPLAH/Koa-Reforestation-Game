import sfml as sf
import src.net as net
import src.res as res

from src.student import Student
from src.teacher import Teacher
from src.farm import FarmServer

import re
import os.path

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Server")
window.key_repeat_enabled = False

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Create the server connection
    server = net.Server(30000)
    
    packets = server.wait_for_connections(1)
    students = {}
    while len(students) < 1:
        for client_id, c_packets in packets.items():
            for packet in c_packets:
                students[client_id] = Student()
                students[client_id].deserialize(packet)
                print("Received")
        packets = server.update()
          
    teacher = Teacher(server)
    farm = FarmServer(server, teacher)
    
    # Check if user exists already
    filename = "content/"+students[client_id].first_name+"_"+students[client_id].last_name+".txt"
    if os.path.isfile(filename): # file exists so user exists
        with open(filename) as file:
            for line in file:
                if re.search(students[client_id].first_name, line):
                    values = line.split()
                    teacher.set_student_points(students[client_id], values[2])
    else:
        print("User", students[client_id].first_name, students[client_id].last_name, "doesn't exist")
        
except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

while True:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update the server
    server.update()

    ## Draw
    
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate) # draw framerate
    farm.draw(window)
    window.display() # update the window
