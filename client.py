import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.users import Student
from src.users import Teacher
from src.login_interface import LoginInterface
from src.farm_state import ClientFarmState
from src.farm_interface import FarmInterface
from src.input_system import InputSystem

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Client")
window.key_repeat_enabled = True

input_sys = InputSystem(window)

# Create the frame rate text
frame_rate = sf.Text("0", res.font_farmville, 20)

# Connect to server
client = net.Client("localhost", 30000)

logged_in = False
login_interface = LoginInterface(client, input_sys)

user = None

while not logged_in and window.is_open:
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate)
    input_sys.handle()
    login_interface.update(0)
    login_interface.draw(window)
    window.display() # update the window
    
    # Receive packets
    packets = client.update()
    for packet in packets:
        packet_id = packet.read()
        if packet_id == const.packet_confirm_login:
            user_type = packet.read()
            if user_type == "Student":
                user = Student(client.client_id)
                user.deserialize(packet)
                farm = ClientFarmState(client, user, input_sys)
                user.state = farm
                user.farm = farm
                user.interface = FarmInterface(client, user, user.state, input_sys)
                # request farm for student
                new_packet = net.Packet()
                new_packet.write(const.packet_request_load_farm)
                name = user.first_name+" "+user.last_name
                new_packet.write(name)
                client.send(new_packet)
            elif user_type == "Teacher":
                user = Teacher(client.client_id)
                user.deserialize(packet)
                user.interface = FarmInterface(client, input_sys)
            logged_in = True
            del login_interface

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
    user.state.update(dt)
    
    # DRAW
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate)
    user.state.draw(window)
    window.display() # update the window
