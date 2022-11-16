import Rhino.Geometry as rg
import simple_ur_script as ur
import simple_comm as c
import json


def UpdateNavigation():
    with open(NAVIGATION_JSON) as f:
        data = json.load(f)







def set_robot_base():
    pt_0 = rg.Point3d(data['origin'][0],data['origin'][1],data['origin'][2]) # base plane origin
    pt_1 = rg.Point3d(data['origin_x'][0],data['origin_x'][1],data['origin_x'][2]) # point on positive x axis
    pt_2 = rg.Point3d(data['origin_y'][0],data['origin_y'][1],data['origin_y'][2]) # point on positive xy plane
    robot_base = rg.Plane(pt_0,pt_1-pt_0,pt_2-pt_0)
    return robot_base



def rhino_to_robot_space(rhino_plane):
    plane = rhino_plane.Clone()
    rhino_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ROBOT_BASE)
    plane.Transform(rhino_matrix)
    return plane

test_plane = debug_plane.Clone()



def send(script):
    script = c.concatenate_script(script)
    c.send_script(script, ROBOT_IP)
    return script

script = ""
script = tcp(script)

if is_debug_mode:
    script += ur.move_l(rhino_to_robot_space(test_plane), SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)


a = ghdoc.Path

path = a.split('3d_printing_teamwork')[0]+r'3d_printing_teamwork\\'+file_name



ROBOT_IP = data['ip']
TCP = data['tcp']
ROBOT_BASE = set_robot_base()


if fabricate:
    send(script)
