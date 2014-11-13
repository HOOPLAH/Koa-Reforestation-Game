# networking stuff

packet_login = 0
packet_confirm_login = 1 # server sends back a confirm/deny login packet
packet_save_student = 2
packet_save_everything = 3
packet_add_points = 4
packet_request_add_inventory = 5
packet_add_inventory = 6
packet_request_place_item = 7 # client sends this to server when he wants to place tree
packet_place_item = 8
packet_request_load_farm = 9
packet_load_farm = 10
packet_request_user_info = 11 # every student's information
packet_load_user_info = 12
