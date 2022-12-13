import Rhino.Geometry as rg
import random as r
from ghpythonlib import treehelpers as th
from copy import deepcopy

def OrientPlane(plane, guide):
    yPt = plane.Origin + rg.Vector3d(0,0,1)
    project = rg.Transform.ProjectAlong(plane,plane.ZAxis)
    yPt.Transform(project)
    yAxis = rg.Vector3d(yPt-plane.Origin)
    
    zAxis = plane.ZAxis
    if zAxis*guide <0: zAxis = -zAxis

    outPlane = rg.Plane(plane.Origin,-rg.Vector3d.CrossProduct(zAxis,yAxis), yAxis)
    return outPlane

def get_pts(crv):
    
    all_pts = []
        
    crv = curve.ToNurbsCurve(curve.Domain)
    params = crv.DivideByCount(divide_number,True)
    
    for i in params:
        pt = crv.PointAt(i)
        all_pts.append(pt)
 
    return all_pts


def make_planes (pts):

    pts_planes = []

    for pt in pts:
        plane = rg.Plane(pt, rg.Vector3d.YAxis)
        pts_planes.append(plane)

    
    ####################################################################
    
    # for j in range(1, len(plns)-1):
    #     plane = rg.Plane(plns[j], plns[j-1], plns[j+1])
    #     new_plane = OrientPlane(plane, rg.Vector3d(1,0,0))
    #     pts_planes.append(new_plane)
    
    return pts_planes
    

def move_planes(plns, plns_graph):

    moved_plns = []
      
    for k, value in enumerate(plns_graph):
        origin = plns[k].Clone()
        trans1 = rg.Transform.Translation(rg.Vector3d(0,plns_graph[k],0))
        origin.Transform(trans1)
        moved_plns.append(origin)
   
    return moved_plns

def make_layered_planes (plns):

    layered_planes = [plns]
    flip = True

    for l in range(layer_nbr):
        temp = []
        for p in layered_planes[l]:
            layer_1 = deepcopy(p)
            trans2 = rg.Transform.Translation(rg.Vector3d(0,layer_height,0))
            layer_1.Transform(trans2)
            temp.append(layer_1)
        if flip:
            temp.reverse
        flip = not flip
        layered_planes.append(temp)

    return layered_planes


pts_divisions = (get_pts(curve))
pts_planes = make_planes(pts_divisions)
moved_planes = move_planes(pts_planes, plns_graph)
layered_planes = th.list_to_tree(make_layered_planes (moved_planes))


    # def get_crvs(self):
    #     cls = []
    #     for i in range(self.cnt):
    #         origin = self.pt.Clone()
    #         T = rg.Transform.Translation(0,0,i*5)
    #         origin.Transform(T)
    #         c = rg.Circle(origin,self.r*graph_map[i])
    #         cls.append(c)
    #     return cls



    # def make_layered_planes (plns):

    # layered_planes = []

    # for list in range(layer_nbr):
    #     temp = []
        
    #     for m in list:
    #         layer_1 = deepcopy(plns[l])
    #         trans2 = rg.Transform.Translation(rg.Vector3d(0,layer_height,0))
    #         layer_1.Transform(trans2)
    #         temp.append(layer_1)
        
    #     layered_planes.append(temp)

    # return layered_planes