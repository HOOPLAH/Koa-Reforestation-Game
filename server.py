import sfml as sf
import src.net as net
import src.res as res

from src.users import Student
from src.users import Teacher
from src.farm import FarmServer

try:
    # Create the server connection
    server = net.Server(30000)
          
    teacher = Teacher(server)
    farm = FarmServer(server, teacher)
        
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
