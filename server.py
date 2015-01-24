import src.net as net
import src.const as const

from src.packet_manager import ServerPacketManager

# Create the server connection
server = net.Server(const.PORT)

packet_manager = ServerPacketManager(server)

while True:
	server.update()
