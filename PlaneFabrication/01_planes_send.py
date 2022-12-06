# import rtde wrapper from current directory
from data import rtde_wrapper_2 as rtde
#from data import rtde_wrapper as rtde

# standard imports
import os
import json

# import sys
# import compas geometry dependencies
from compas.geometry import Frame, Vector, Point, Transformation, Translation
from compas.data import json_load

with open(r"PlaneFabrication\data\master_navigation_data.json", "r") as f:
    data = json.load(f)


origin = data["origin"]
origin_x = data["origin_x"]
origin_y = data["origin_y"]
tcp = data["tcp"]
Z_OFFSET = data["offset_z"]

#########################################################
# Define constant parameters
MAX_SPEED = 50.00  # mm/s float
MAX_ACCEL = 50.00  # mm/s2 float
IP_ADDRESS = data["ip"]  # string with IP Address
##########################################################

# Define location of print data
# change .json file path and name as required   
DATA_OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "data", "output")
PRINT_FILE_NAME = "out_printpoints.json"

# Open print data
with open(os.path.join(DATA_OUTPUT_FOLDER, PRINT_FILE_NAME), "r") as file:
    data = json.load(file)
print("Print data loaded :", os.path.join(DATA_OUTPUT_FOLDER, PRINT_FILE_NAME))

####################################################################
# Define print data containers as empty lists
planes = json_load(r"PlaneFabrication\data\output\out_printpoints.json")
frames = []
for lists in planes:
    for list in lists:
        small_list=[]
        for p in list:
            print (p)
            small_list.append(Frame.from_plane(p))
    frames.append(small_list)


velocities = [[20] *len(frames[0])]* len(frames)
radii = [[5] * len(frames[0])]* len(frames)
toggles = [[0] * len(frames[0])]* len(frames)

for list in toggles:
    list[-1]=2

#toggles = [0,0,0,2,0,0,0,0]
#toggles = [True]*(len(frames))
# Go through JSON and copy data to lists
# for item in data:
# Read frame data
# point = data[item]['frame']['point']
# xaxis = data[item]['frame']['xaxis']
# yaxis = data[item]['frame']['yaxis']

# Fill containers for velocities

#     frames.append(frame)
#     velocities.append(data[item]['velocity'])
#     radii.append(data[item]['blend_radius'])
#     toggles.append(data[item]['extruder_toggle'])
# #######################################################################


# Use the data to execute the printpath
if __name__ == "__main__":
    print (velocities, toggles, radii)
    # Create base frame with measured points
    ORIGIN = Point(origin[0], origin[1], origin[2])
    XAXIS_PT = Point(origin_x[0], origin_x[1], origin_x[2])
    YAXIS_PT = Point(origin_y[0], origin_y[1], origin_y[2])
    # Create a compas Frame
    base_frame = Frame.from_points(ORIGIN, XAXIS_PT, YAXIS_PT)
    # base_frame = Frame(Point(548.032, 552.647, -2.884), Vector(-1.000, -0.013, 0.002), Vector(0.013, -1.000, 0.003))

    i=0
    for frame_list in frames:

        # Transform all frames from slicing location to robot coordinate system
        T = Transformation.from_frame_to_frame(Frame.worldXY(), base_frame)
        frame_list = [f.transformed(T) for f in frame_list]

        # Move frames by a Z fine tuning parameter as required
        T = Translation.from_vector([0, 0, Z_OFFSET])
        frame_list = [f.transformed(T) for f in frame_list]

        # IP_ADDRESS = "127.0.0.1"
        # Send all points using send_printpath function implemented in the RTDE Wrapper
        rtde.send_printpath(frame_list, velocities[i], MAX_ACCEL, radii[i], toggles[i], ip=IP_ADDRESS)
        i+=1
