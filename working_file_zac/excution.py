import Rhino.Geometry as rg
import simple_ur_script as ur
import simple_comm as c
import json


def set_robot_base():
    pt_0 = rg.Point3d(data["origin"][0], data["origin"][1], data["origin"][2])  # base plane origin
    pt_1 = rg.Point3d(
        data["origin_x"][0], data["origin_x"][1], data["origin_x"][2]
    )  # point on positive x axis
    pt_2 = rg.Point3d(
        data["origin_y"][0], data["origin_y"][1], data["origin_y"][2]
    )  # point on positive xy plane
    robot_base = rg.Plane(pt_0, pt_1 - pt_0, pt_2 - pt_0)
    return robot_base


def rhino_to_robot_space(rhino_plane):
    plane = rhino_plane.Clone()
    rhino_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ROBOT_BASE)
    plane.Transform(rhino_matrix)
    return plane


def send(script):
    script = c.concatenate_script(script)
    c.send_script(script, ROBOT_IP)
    return script




script = ""
data = []
with open(NAVIGATION_JSON, "r") as f:
    data = json.load(f)
TCP = data["tcp"]
ROBOT_IP = data["ip"]
ROBOT_BASE = set_robot_base()
script += ur.set_tcp_by_angles(TCP[0], TCP[1], TCP[2], TCP[3], TCP[4], TCP[5])

if send_debug_plane:
    for debug_plane in debug_planes:
        script += ur.move_l(rhino_to_robot_space(debug_plane), DEBUG_ROBOT_ACC, DEBUG_ROBOT_VEL)
    send(script)
