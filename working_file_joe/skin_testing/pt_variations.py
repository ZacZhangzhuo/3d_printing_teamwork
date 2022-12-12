import Rhino.Geometry as rg
from ghpythonlib import treehelpers as th

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
        
    crv_length = curve.GetLength()
    count = int(crv_length/divide_interval)
    crv = curve.ToNurbsCurve(curve.Domain)
    params = crv.DivideByCount(count,True)
    
    for i in params:
        pt = crv.PointAt(i)
        # new_pln = rg.Plane(pln.Origin, pln.XAxis, pln.ZAxis)
        # new_pln = OrientPlane(new_pln, rg.Vector3d(0,1,0))
        # print (type(pln))
        all_pts.append(pt)
        # planes.append(new_pln)
            
    return all_pts


def make_planes (plns):

    pts_planes = []

    for j in range(1, len(plns)-1):
        plane = rg.Plane(plns[j], plns[j-1], plns[j+1])
        new_plane = OrientPlane(plane, rg.Vector3d(0,1,0))
        pts_planes.append(new_plane)
    
    return pts_planes
    

# def offset_layers(pts):

#     layerd_pts = []

#     for i in range(layer_nbr):
#         temp = []
#         pole_circ = []
        
#         for j, value in enumerate(pt_graph):
#             pole_center_plane = rg.Plane(pts[j][i], rg.Vector3d.CrossProduct(rg.Vector3d.ZAxis,y_axis[j][i]), y_axis[j][i])
#             temp.append(pole_rect)
#         pole = rg.Brep.CreateFromLoft(temp, rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType(1),False)
#         poles.append(pole)

pts_divisions = (get_pts(curve))
pts_planes = make_planes(pts_divisions)

