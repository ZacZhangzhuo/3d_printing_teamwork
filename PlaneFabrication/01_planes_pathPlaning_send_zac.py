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
rtde.send_configs(c, 0.3, 1.0,  0.001, toggles= False , ip = IP_ADDRESS)


# ur_c = RTDEControl(IP_ADDRESS)
# ur_c.moveJ([0.873, -1.222, -2.793, 0.262, 1.571, -3.142], 0.8, 0.5, 0) #! Configuration_2


# toggles = []
# for t in range(len(frames)):
#     if t % 11 == 0:
#         toggles.append(1)
#     else:
#         toggles.append(0)
# #toggles = [0,0,0,2,0,0,0,0]
# #toggles = [True]*(len(frames))
# # Go through JSON and copy data to lists
# # for item in data:
# # Read frame data
# # point = data[item]['frame']['point']
# # xaxis = data[item]['frame']['xaxis']
# # yaxis = data[item]['frame']['yaxis']
# # Fill containers for velocities

# #     frames.append(frame)
# #     velocities.append(data[item]['velocity'])
# #     radii.append(data[item]['blend_radius'])
# #     toggles.append(data[item]['extruder_toggle'])
# # #######################################################################


# # Use the data to execute the printpath
# if __name__ == "__main__":
#     # Create base frame with measured points
#     ORIGIN = Point(origin[0], origin[1], origin[2])
#     XAXIS_PT = Point(origin_x[0], origin_x[1], origin_x[2])
#     YAXIS_PT = Point(origin_y[0], origin_y[1], origin_y[2])
#     # Create a compas Frame
#     base_frame = Frame.from_points(ORIGIN, XAXIS_PT, YAXIS_PT)
#     # base_frame = Frame(Point(548.032, 552.647, -2.884), Vector(-1.000, -0.013, 0.002), Vector(0.013, -1.000, 0.003))

#     # Transform all frames from slicing location to robot coordinate system
#     T = Transformation.from_frame_to_frame(Frame.worldXY(), base_frame)
#     frames = [f.transformed(T) for f in frames]

#     # Move frames by a Z fine tuning parameter as required
#     T = Translation.from_vector([0, 0, Z_OFFSET])
#     frames = [f.transformed(T) for f in frames]

#     # IP_ADDRESS = "127.0.0.1"
#     # Send all points using send_printpath function implemented in the RTDE Wrapper
#     rtde.send_printpath(frames, velocities, MAX_ACCEL, radii, toggles, ip=IP_ADDRESS)
