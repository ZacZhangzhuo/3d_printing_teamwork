import Rhino.Geometry as rg
import random as r
import ghpythonlib as ghc
from ghpythonlib import treehelpers as th
from copy import deepcopy
import math


def OrientPlane(plane, guide):
    yPt = plane.Origin + rg.Vector3d(0, 0, 1)
    project = rg.Transform.ProjectAlong(plane, plane.ZAxis)
    yPt.Transform(project)
    yAxis = rg.Vector3d(yPt-plane.Origin)

    zAxis = plane.ZAxis
    if zAxis*guide < 0:
        zAxis = -zAxis

    outPlane = rg.Plane(
        plane.Origin, -rg.Vector3d.CrossProduct(zAxis, yAxis), yAxis)
    return outPlane

def Remap(value, min, max, new_min, new_max):
    
    old_range = max - min
    new_range = new_max - new_min
    
    return (((value - min)* new_range)/ old_range) + new_min

def get_pts(crv):

    all_pts = []

    crv = curve.ToNurbsCurve(curve.Domain)
    # params = crv.DivideByCount(divide_number, True)

    params = crv.DivideByCount(6, True)
    # print(len(params))

    for i in params:
        pt = crv.PointAt(i)
        all_pts.append(pt)

    return all_pts


def make_planes(pts):

    pts_planes = []

    for k, pt in enumerate(pts):
        point, uv_pt, distance = ghc.components.SurfaceClosestPoint(pt, srf)
        pnt, normal, u, v, f = ghc.components.EvaluateSurface(srf, uv_pt)
        plane = rg.Plane(pt, rg.Vector3d(u), rg.Vector3d(v))
        rg.Plane.Rotate(plane, math.radians(-90), plane.ZAxis, plane.Origin)

        # halfLength = len(pts)/2
        # rotation2 = rg.Transform.Rotation((((abs(halfLength-k))/halfLength)*-math.pi*0.5), plane.Normal, plane.Origin)
        # rotation2 = rg.Transform.Rotation(((len(pts)-k)*math.pi/len(pts) + -math.pi*0.5), plane.Normal, plane.Origin)
        # plane.Transform(rotation2)
        pts_planes.append(plane)
    return pts_planes


def move_planes(plns, pt, min_layer_height, max_layer_height):

    # for pln in plns:
    #     if pt.DistanceTo(pln.Origin) <= min_dist:
    #         min_dist = new_min_dist
        
    #     if pt.DistanceTo(pln.origin) <= max_dist:
    #         max_dist = new_max_dist
        
    
    heights = []
    
    for pln in plns:
        
        heights.append(Remap(pt.DistanceTo(pln.Origin), min_dist, max_dist, max_layer_height, min_layer_height))
    
    if flip_vect:
        for i in range(len(plns)):
            plns[i] = rg.Plane(
                plns[i].Origin, -plns[i].XAxis, plns[i].YAxis)
        # print (new_layer_height)
        # new_layer_height = -new_layer_height
        # print (new_layer_height)
    
    moved_plns = [plns]
    
    print(moved_plns)

    for l in range(layer_nbr):
        temp = []
        for i, p in enumerate(moved_plns[l]):
            origin = deepcopy(p)
            trans1 = rg.Transform.Translation(
                rg.Vector3d(p.ZAxis*heights[i]))
            origin.Transform(trans1)
            moved_plns.append(origin)
        temp.reverse()
        
        moved_plns.append(temp)

    return moved_plns 


# def make_layered_planes(plns, plns_heights):

    
 

#     for l in range(layer_nbr):
#         temp = []
#         for i, p in enumerate(layered_planes[l]):
#             layer_1 = deepcopy(p)
#             trans2 = rg.Transform.Translation(
#                 rg.Vector3d(p.Normal*plns_heights[i]))
#             layer_1.Transform(trans2)
#             temp.append(layer_1)



#     return layered_planes

# print(layer_height)
pts_divisions = (get_pts(curve))
pts_planes = make_planes(pts_divisions)
# print (pts_planes)
moved_planes =th.list_to_tree(move_planes(pts_planes, plns_move_pt, max_layer_height, min_layer_height))
# layered_planes = (make_layered_planes(moved_planes, heights))
