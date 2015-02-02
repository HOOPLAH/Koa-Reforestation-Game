import random
from enum import IntEnum

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480

PORT = 50002

class GameStates(IntEnum):
	LOGIN = 0
	HOME_FARM = 1
	GUEST_FARM = 2
	TEACHER_GUEST_FARM = 3
	SHOP = 4
	STATS = 5

class PacketTypes(IntEnum):
    LOGIN = 0
    ADD_FARM_ITEM = 1
    ADD_INVENTORY_ITEM = 2
    SWITCH_FARM = 3
    LOAD_FARM = 4
    SAVE_FARM = 5
    ADD_POINTS = 6
    SET_POINTS = 7
    GET_USER = 8