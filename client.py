import sfml as sf
import src.net as net

from src.input_system import InputSystem
from src.GUI.gui_manager import GUIManager

from src.states.state import GameStates
from src.states.login_state import LoginState

from src.user import User

# create the main window
window = sf.RenderWindow(sf.VideoMode(800, 480), "Koa Reforestation Client")

# Connect to server
client = net.Client("localhost", 50001)

input_sys = InputSystem(window)
gui = GUIManager()
user = User(client, "")

# make all the states
login_state = LoginState(client, input_sys, gui, user)

user.states = [login_state]
user.state = GameStates.LOGIN

clock = sf.Clock()

# start the game loop
while window.is_open:
    dt = clock.restart().seconds
    
    client.update()
    input_sys.handle()
    user.update(dt)

    window.clear() # clear screen
    user.render(window)
    window.display() # update the window
