#to reload the simple ur script and simple comm modules
from compas_rhino import unload_modules
unload_modules('simple_ur_script')
unload_modules('simple_comm')

#import all necessary modules
import Rhino.Geometry as rg
import simple_comm as c
import simple_ur_script as ur
import math as m


def tcp(script):
    """ 
    This function sets tcp of the robot
    variables : [x,y,z,ry,ry,rz] 
    x, y, z : point coordinates (float)
    ry, ry, rz : euler angles for rotation
    """
    script += ur.set_tcp_by_angles(float(15.76), float(-47.24), float(143.04 + myTCP_z), m.radians(0.0), m.radians(180.0), m.radians(90.0))
    return script
#    script += ur.set_tcp_by_angles(float(15.76), float(-47.24), float(143.04), m.radians(0.0), m.radians(180.0), m.radians(90.0))
def set_robot_base_plane_from_pts(ori_pt, xAxis_pt, yAxis_pt):
    """
    set robot base from measured points
    ori_pt : origin
    xAxis_pt : point on the positive x axis
    yAxis_pt : point on the positive XY plane
    """
    robot_base = rg.Plane(ori_pt, xAxis_pt - ori_pt, yAxis_pt - ori_pt)
    return robot_base

def rhino_to_robot_space(rhino_plane):
    """ this funktion translates planes from the rhino cordinate system to
    the robot cordinate system 
    """
    robot_plane = rhino_plane.Clone()
    robotBase_plane = set_robot_base_plane_from_pts(ori_pt, xAxis_pt, yAxis_pt)
    _r_matrix = rg.Transform.PlaneToPlane(rg.Plane(inputBase_pt, rg.Vector3d.XAxis, rg.Vector3d.YAxis), 
                                          robotBase_plane)
    robot_plane.Transform(_r_matrix)
    return robot_plane

def point_to_rhino_plane(point):
    """
    create a standard XY plane from a point
    """
    rhino_plane = rg.Plane(point, -rg.Vector3d.XAxis, -rg.Vector3d.YAxis)
    return rhino_plane

def set_extruder_speed_1(script):
    #turn OFF IO 5 to turn on any extrusion
    script += ur.set_digital_out(5, False)
    #extruder auto speed 1 (aspeed 1 in arduino) is connected to Digital IO 6
    script += ur.set_digital_out(6,True) 
    #make sure IO 7 is off
    script += ur.set_digital_out(7,False)
    #add required lines to script and return
    return script
    
def set_extruder_speed_2(script):
    #turn OFF IO 5 to turn on any extrusion
    script += ur.set_digital_out(5, False)
    #extruder auto speed 1 (aspeed 1 in arduino) is connected to Digital IO 6
    script += ur.set_digital_out(6,False) 
    #extruder auto speed 2 (aspeed 0 in arduino) is connected to Digital IO 7
    script += ur.set_digital_out(7,True)
    return script

def set_extruder_retraction(script):
    #turn OFF IO 5 to turn on any extrusion
    script += ur.set_digital_out(5, False)
    #retraction can be triggered by turning on IO 6 and 7 both
    script += ur.set_digital_out(6, True) 
    script += ur.set_digital_out(7, True)
    #add required lines to script and return
    return script
    
def extrude(plane, vel, blend_radi, extr, script, change_extruder_status):
    #move to desired plane
    script += ur.move_l_blend(plane, vel/1000, blend_radi/1000)
    #check if extruder needs to be toggled, if yes, then check if it is True or False
    if change_extruder_status:
        #if true, then set extruder speed, to turn on the extruder
        if extr:
            #script = set_extruder_speed_1(script)
            script = set_extruder_speed_2(script)
        #otherwise, turn it off by turning on IO 5
        else:
            script += ur.set_digital_out(5, True) 
    return script 

############################################################################################################
# Robotic fabrication procedure
############################################################################################################

# if __name__ == '__main__':
script = "" #c=reate empty string for script
#set TCP from script if required
#script = tcp(script)

#Create rhino planes
rhino_base_way_planes = []
for point in robot_pts:
    rhino_base_way_planes.append(point_to_rhino_plane(point)) #create a list of standard XY planes

#Translate rhino planes to robot_plane 
robot_planes = []
for rhino_plane in (rhino_base_way_planes):
    robot_planes.append(rhino_to_robot_space(rhino_plane))
    
#create extruder commands
change_extruder_status = True #default value for state change flag
#Iterate through all lists; notice use of enumerate and zip together
for i, (plane, velocity, blend_radi, extruder_toggle) in enumerate(zip(robot_planes, velocities, blend_radii, extruder_toggles)):
    #for every plane after plane 0
    if i>0:
        if extruder_toggle != extruder_toggles[i-1]:
        #if current extruder toggle is not the same as the last one, means extruder state needs to be toggled
            change_extruder_status = True
        else: 
        #otherwise this flag can be False
            change_extruder_status = False
    #go to extrude function to check if extruder is needed to be turned ON
    script = extrude(plane, velocity, blend_radi, extruder_toggle, script, change_extruder_status)
    #for every 5th point, send a log message to the UR controller(helps to know what point you are currently on)
    if i%5 == 0:
        script += ur.textmsg("Pt: %d" % i)
    #For the last point, we send to the last point, and then send to a safe point
    if i == len(robot_pts)-1: 
        script = extrude(plane, velocity, blend_radi, 0, script, change_extruder_status)
        script += ur.move_l_blend(rg.Plane(safe_pt, rg.Vector3d.XAxis, rg.Vector3d.YAxis), velocity/1000, blend_radi/1000)


#send the stuff to robot on button press
if send:
    script = c.concatenate_script(script) #concatenate script before sending
    c.send_script(script, "192.168.10.10") #send to robot #192.168.10.10