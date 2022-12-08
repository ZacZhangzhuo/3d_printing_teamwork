from data import rtde_wrapper_zac as rtde
import os
import json
from compas.geometry import Frame, Vector, Point, Transformation, Translation
from compas.data import json_load
from compas.robots import Configuration
import math
from rtde_control import RTDEControlInterface as RTDEControl


with open(r"PlaneFabrication\data\master_navigation_data.json", "r") as f:
    data = json.load(f)

origin = data["origin"]
origin_x = data["origin_x"]
origin_y = data["origin_y"]
tcp = data["tcp"]
Z_OFFSET = data["offset_z"]

# #########################################################
# Define constant parameters
IP_ADDRESS = data["ip"]  # string with IP Address
# ##########################################################

# Define location of print data
# change .json file path and name as required
DATA_OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "data", "output")
PRINT_FILE_NAME = "out_printpoints.json"

# Open print data
with open(os.path.join(DATA_OUTPUT_FOLDER, PRINT_FILE_NAME), "r") as file:
    data = json.load(file)
print("Print data loaded :", os.path.join(DATA_OUTPUT_FOLDER, PRINT_FILE_NAME))

# ####################################################################
# Define print data containers as empty lists
configs = json_load(r"PlaneFabrication\data\output\out_printpoints.json")

velocities = [0.1] * len(configs)
acc = [0.1] * len(configs)
wait = [2] * len(configs)
blend = [0] * len(configs)


c = []
for i in range(len(configs)):
    # Configuration.joint_dict
    c.append(
        [
            configs[i].joint_dict["shoulder_pan_joint"],
            configs[i].joint_dict["shoulder_lift_joint"],
            configs[i].joint_dict["elbow_joint"],
            configs[i].joint_dict["wrist_1_joint"],
            configs[i].joint_dict["wrist_2_joint"],
            configs[i].joint_dict["wrist_3_joint"],
        ]
    )
    # print(c)




# ur_c = RTDEControl(IP_ADDRESS)
# ur_c.moveJ([0.873, -1.222, -2.793, 0.262, 1.571, -3.142], 0.8, 0.5, 0) #! Configuration_2
rtde.send_configs(c, 0.1, 0.1,  0.001, toggles= True , ip = IP_ADDRESS)



