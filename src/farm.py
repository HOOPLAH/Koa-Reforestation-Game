import sfml as sf
import src.net as net
import src.res as res
import src.const as const

class FarmLandItem: # something placeable on the farm (ex. trees)
    def __init__(self, path, pos):
        self.path = path # need path to identify when sending to server
        self.texture = sf.Texture.from_file(self.path)
        self.sprite = sf.Sprite(self.texture)
        self.position = pos
        
    def draw(self, target):
        target.draw(self.sprite)
        
    def send_item(self, client):
        packet = net.Packet()
        packet.write(const.packet_send_resource)
        packet.write(self.path)
        packet.write(self.position.x)
        packet.write(self.position.y)
        client.send(packet)

class FarmClient:
    def __init__(self, client, student):
        self.client = client
        client.add_handler(self)
        
        self.student_owner = student # the owner of the farm
        
        self.land_items = []
        test = FarmLandItem("content/textures/tree.png", sf.Vector2(32, 32))
        self.land_items.append(test)
        #test.send_item(self.client)
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.packet_add_points:
            self.student_owner.points = packet.read()
            print(self.student_owner.first_name, "'s points:", self.student_owner.points)
    
    def draw(self, target):
        points = sf.Text("0", res.font_8bit, 20)
        points.position = sf.Vector2(760, 0)
        points.string = str(self.student_owner.points)
        target.draw(points)
        
        for item in self.land_items:
            item.draw(target)
            

class FarmServer:
    def __init__(self, server, teacher):
        self.server = server
        self.teacher = teacher
        
        server.add_handler(self)
        
        self.land_items = []
        
    def handle_packet(self, packet):
        packet_id = packet.read()
        
        if packet_id == const.packet_send_resource:
            path = packet.read()
            pos_x = packet.read()
            pos_y = packet.read()
            new_res = FarmLandItem(path, sf.Vector2(pos_x, pos_y))
            self.land_items.append(new_res)