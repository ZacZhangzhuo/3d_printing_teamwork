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
    yAxis = rg.Vector3d(yPt - plane.Origin)

    zAxis = plane.ZAxis
    if zAxis * guide < 0:
        zAxis = -zAxis

    outPlane = rg.Plane(plane.Origin, -rg.Vector3d.CrossProduct(zAxis, yAxis), yAxis)
    return outPlane


def Remap(old_value, old_min, old_max, new_min, new_max):
    # print('x')
    # print (old_value)
    new_value = (old_value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min
    # else
    # print('y')
    # print (new_value)
    return new_value


def get_pts(crvs):

    # Make into loop for list of curves
    all_pts = []

    crv = curve.ToNurbsCurve(curve.Domain)
    # params = crv.DivideByCount(divide_number, True)

    params = crv.DivideByCount(divide_number, True)
    # print(len(params))

    for i in params:
        pt = crv.PointAt(i)
        all_pts.append(pt)

    return all_pts


def make_planes(pts):

    pts_planes = []

    # Make into loop for list of curves

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


def move_planes(plns, height_pt, dir_pt, min_layer_height, max_layer_height, layer_number):

    min_dist = 1000000
    max_dist = 0

    for pln in plns:
        if height_pt.DistanceTo(pln.Origin) < min_dist:
            min_dist = height_pt.DistanceTo(pln.Origin)
        if height_pt.DistanceTo(pln.Origin) > max_dist:
            max_dist = height_pt.DistanceTo(pln.Origin)

    heights = []

    for pln in plns:
        #        print(pt.DistanceTo(pln.Origin))
        temp = Remap(
            height_pt.DistanceTo(pln.Origin), max_dist, min_dist, min_layer_height, max_layer_height
        )
        heights.append(temp)

    #    print(max_dist)

    moved_plns = []


    for i in range(layer_number):


        temp = []
        for k, value in enumerate(heights):
            origin = plns[k].Clone()

            # Trans1.0
            # trans1 = rg.Transform.Translation(rg.Vector3d(plns[k].Normal*heights[k]*i))

            # Trans1.1
            dir = rg.Vector3d(plns[k].Origin - dir_pt)
            dir.Unitize()
            index = (int) (math.floor(Remap(heights[k], min_dist, max_dist, 0, len(plns))))

            trans1 = rg.Transform.Translation((dir * heights[k] * i * graphMapper[index]))

            origin.Transform(trans1)
            temp.append(origin)

        if i%2 ==0: temp.reverse()
        moved_plns.extend(temp)
        # print (max_layer_height)

    return moved_plns


# def make_layered_planes(plns):

#     if flip_vect:
#         for i in range(len(plns)):
#             plns[i] = rg.Plane(
#                 plns[i].Origin, -plns[i].XAxis, plns[i].YAxis)
#         # print (new_layer_height)
#         # new_layer_height = -new_layer_height
#         # print (new_layer_height)
#     layered_planes = [plns]

#     for l in range(layer_nbr):
#         temp = []
#         for i, p in enumerate(layered_planes[l]):
#             layer_1 = deepcopy(p)
#             trans2 = rg.Transform.Translation(
#                 rg.Vector3d(p.Normal*layer_height))
#             layer_1.Transform(trans2)
#             temp.append(layer_1)

#         temp.reverse()
#         layered_planes.append(temp)

#     return layered_planes

# list_pts = th.tree_to_list(list_pts)
# print(layer_height)
# pts_divisions = (get_pts(curve))

pts_planes = make_planes(list_pts)
# print (pts_planes)

moved_planes = move_planes(
    pts_planes,
    height_pt=plns_height_pt,
    dir_pt=plns_dir_pt,
    min_layer_height=min_layer_height,
    max_layer_height=max_layer_height,
    layer_number=layer_nbr,
)

# layered_planes = th.list_to_tree(make_layered_planes(pts_planes))
