
from data import rtde_wrapper as rtde


with open(r'simulation_visualization_fabrication\data\master_navigation_data.json', "r") as f:
    data = json.load(f)

origin = data["origin"]
origin_x = data["origin_x"]
origin_y = data["origin_y"]
tcp = data["tcp"]
Z_OFFSET = data["offset_z"]
MAX_SPEED = 50.00 #mm/s float
MAX_ACCEL = 100.00 #mm/s2 float
IP_ADDRESS = data["ip"]#string with IP Address


rtde.send_printpath(frames, velocities, MAX_ACCEL , radii, toggles, ip=IP_ADDRESS)