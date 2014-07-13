import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.student import Student
from src.farm import FarmClient
from src.farm_interface import FarmInterface
from src.input_system import InputSystem

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Client")
window.key_repeat_enabled = False

input_sys = InputSystem(window)

try:
    # Create the frame rate text
    frame_rate = sf.Text("0", res.font_8bit, 20)

    # Connect to server
    client = net.Client("localhost", 30000)
    
    student = Student(client.client_id)
    student.first_name = input("first: ")
    student.last_name = input("last: ")
    
    # Send the server my info
    login_packet = net.Packet()
    student.serialize(login_packet)
    client.send(login_packet)
    client.update()
    
    farm_interface = FarmInterface(client, student)
    farm = FarmClient(input_sys, farm_interface, client, student)

except IOError:
    exit(1)

clock = sf.Clock()
frame_accum = 0
dt_accum = 0

# start the game loop
while window.is_open:
    dt = clock.restart().seconds
    
    # Calculate framerate
    frame_accum += 1
    dt_accum += dt
    if dt_accum >= 1:
        frame_rate.string = str(frame_accum)
        dt_accum = 0
        frame_accum = 0

    # Update connection
    client.update()
    
    farm.update(dt)
    
    # DRAW
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate)
    farm.draw(window)
    window.display() # update the window