import src.net as net

from src.packet_manager import ServerPacketManager

# Create the server connection
server = net.Server(50001)

packet_manager = ServerPacketManager(server)

while True:
	server.update()
