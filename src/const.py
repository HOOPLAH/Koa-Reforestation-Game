import random
from enum import IntEnum

class GameStates(IntEnum):
	LOGIN = 0
	HOME_FARM = 1
	GUEST_FARM = 2
	SHOP = 3
	STATISTICS = 4

class PacketTypes(IntEnum):
    LOGIN = 0
    ADD_FARM_ITEM = 1
    ADD_INVENTORY_ITEM = 2
    SWITCH_FARM = 3
    LOAD_FARM = 4

PORT = 50002