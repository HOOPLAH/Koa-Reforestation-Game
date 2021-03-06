import sfml as sf
import src.net as net
import src.const as const

from src.input_system import InputSystem
from src.GUI.gui_manager import GUIManager

from src.states.login_state import LoginState
from src.states.farm_state import HomeFarmState
from src.states.farm_state import GuestFarmState
from src.states.farm_state import TeacherGuestFarmState
from src.states.shop_state import ShopState
from src.states.statistics_state import StatisticsState

from src.user import User

# create the main window
window = sf.RenderWindow(sf.VideoMode(const.WINDOW_WIDTH, const.WINDOW_HEIGHT), "Koa Reforestation Client")

# Connect to server
client = net.Client("localhost", const.PORT)

input_sys = InputSystem(window)
gui = GUIManager()
user = User(client, "")

# make all the states
login = LoginState(client, input_sys, gui, user)
home = HomeFarmState(client, input_sys, gui, user)
guest = GuestFarmState(client, input_sys, gui, user)
teacher = TeacherGuestFarmState(client, input_sys, gui, user)
shop = ShopState(client, input_sys, gui, user)
stats = StatisticsState(client, input_sys, gui, user)

user.states = [login, home, guest, teacher, shop, stats]
user.state = const.GameStates.LOGIN
user.states[user.state].init()

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
