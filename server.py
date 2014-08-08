import sfml as sf
import src.net as net
import src.res as res

from src.users import Student
from src.users import Teacher
from src.farm_state import ServerFarmState

# Create the server connection
server = net.Server(30000)

users = {}
filename = "content/users/all_registered_users.txt"
file = open(filename, 'r')
for line in file:
    values = line.split()
    if values[2] == "Student":
        users[values[0]] = Student(None) # empty student, found by first name
        users[values[0]].first_name = values[0]
        users[values[0]].last_name = values[1]
    elif values[2] == "Teacher":
        users[values[0]] = Teacher(None, server) # empty teacher
        users[values[0]].first_name = values[0]
        users[values[0]].last_name = values[1]
        
farm = ServerFarmState(server, users)
        

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

while True:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        dt_accum = 0
        frame_accum = 0

    # Update the server
    server.update()
