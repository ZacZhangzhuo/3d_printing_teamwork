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


def get_pts(crv):

    all_pts = []

    crv = curve.ToNurbsCurve(curve.Domain)
    # params = crv.DivideByCount(divide_number, True)
    params = crv.DivideByCount(2, True)


    for i in params:
        pt = crv.PointAt(i)
        all_pts.append(pt)

    return all_pts


def make_planes(pts):

    pts_planes = []

    for pt in pts:
        point, uv_pt, distance = ghc.components.SurfaceClosestPoint(pt, srf)
        pnt, normal, u, v, f = ghc.components.EvaluateSurface(srf, uv_pt)
        plane = rg.Plane(pt, rg.Vector3d(u), rg.Vector3d(v))
        rg.Plane.Rotate(plane, math.radians(-90), plane.ZAxis, plane.Origin)
        pts_planes.append(plane)

    return pts_planes


# def move_planes(plns, plns_graph):

#     moved_plns = []

#     for k, value in enumerate(plns_graph):
#         origin = plns[k].Clone()
#         trans1 = rg.Transform.Translation(
#             rg.Vector3d(plns[k].Normal*plns_graph[k]))
#         origin.Transform(trans1)
#         moved_plns.append(origin)

#     return moved_plns


def make_layered_planes(plns, new_layer_height):

    
    if flip_vect:
        for i in range(len(plns)):
            plns[i] = rg.Plane(
                plns[i].Origin, -plns[i].XAxis, plns[i].YAxis)
        # print (new_layer_height)
        # new_layer_height = -new_layer_height
        # print (new_layer_height)
    layered_planes = [plns]

    for l in range(layer_nbr):
        temp = []
        for i, p in enumerate(layered_planes[l]):
            layer_1 = deepcopy(p)
            trans2 = rg.Transform.Translation(
                rg.Vector3d(p.Normal*new_layer_height*plns_graph[i]))
            layer_1.Transform(trans2)
            temp.append(layer_1)

        temp.reverse()
        layered_planes.append(temp)

    return layered_planes

print(layer_height)
pts_divisions = (get_pts(curve))
pts_planes = make_planes(pts_divisions)
print (pts_planes)
# moved_planes = move_planes(pts_planes, plns_graph)
layered_planes = th.list_to_tree(make_layered_planes(pts_planes, layer_height))
