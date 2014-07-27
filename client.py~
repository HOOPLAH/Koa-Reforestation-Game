import sfml as sf
import src.net as net
import src.res as res
import src.const as const

from src.users import Student
from src.users import Teacher
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
    
    first_name = "Lucas"
    last_name = "DeRego"
    
    # Send the server my info
    logged_in = False
    login_packet = net.Packet()
    login_packet.write(const.packet_login)
    login_packet.write(first_name)
    login_packet.write(last_name)
    client.send(login_packet)
    client.update()
    
    # Wait for confirm packet from server
    while not logged_in:
        packets = client.update()
        for packet in packets:
            packet_id = packet.read()
            if packet_id == const.packet_confirm_login:
                user_type = packet.read()
                if user_type == "Student":
                    student = Student(client.client_id)
                    student.deserialize(packet)
                    student.farm = FarmClient(client, student, input_sys)
                    student.farm_interface = FarmInterface(client, student, student.farm, input_sys)
                    # request farm for student
                    new_packet = net.Packet()
                    new_packet.write(const.packet_request_load_farm)
                    new_packet.write(client.client_id)
                    client.send(new_packet)
                elif user_type == "Teacher":
                    teacher = Teacher(client.client_id)
                    teacher.deserialize(packet)
                    teacher.farm_interface = FarmInterface(client, teacher, input_sys)
                logged_in = True
            elif packet_id == const.packet_deny_login:
                print(packet.read())
                exit(1)

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
    
    student.farm.update(dt)
    
    # DRAW
    window.clear(sf.Color(120, 120, 120)) # clear screen
    window.draw(frame_rate)
    student.farm_interface.draw(window)
    window.display() # update the window
