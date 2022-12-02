import Rhino.Geometry as rg
import ghpythonlib
import math


layer_cnt = int(brep_height/layer_thickness)
contours = []
contour_srf = []
contour_arc = []


for i, value in enumerate(graph_val):
    center_pt = origin_pt + rg.Vector3d(0,0,i*layer_thickness)
    #use the rg.vector to create the world xy origin, but not have it exist relation to the origin
    center_plane = rg.Plane(center_pt, rg.Vector3d.XAxis, rg.Vector3d.YAxis)
    contour = rg.Circle(center_plane, radius*graph_val[i])
    contour.Rotate(math.radians(i*rot_angle),rg.Vector3d.ZAxis)
    cont_arc = rg.ArcCurve(contour)
    contour_arc.append(cont_arc)
    contours.append(contour)
contour_srf = rg.Brep.CreateFromLoft(contour_arc, rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType(1),False)


pts= []

for c in contours:
    cont_pts = []
    crv = c.ToNurbsCurve(2,5)
    params = crv.DivideByCount(pole_count, True)
    for i in params:
        pt = crv.PointAt(i)
        cont_pts.append(pt)
    pts.append(cont_pts)

poles = []
pole_crvs = []


for i in range(pole_count):
    temp = []
    pole_circ = []
    for j, value in enumerate(pole_graph):
        pole_center_plane = rg.Plane(pts[j][i], rg.Vector3d.XAxis, rg.Vector3d.YAxis)
        pole_rad= rg.Circle(pole_center_plane, pole_rad_val*(0.5*pole_graph[j]))
        pole_arc = rg.ArcCurve(pole_rad)
        temp.append(pole_arc)
        pole_circ.append(pole_rad)
    pole = rg.Brep.CreateFromLoft(temp, rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType(1),False)
    pole_crvs.append(pole_circ)
    poles.append(pole)

edge_pts = []

for list in pole_crvs:
    circ_pts = []
    for arc in list:
        crv = arc.ToNurbsCurve(2,5)
        params = crv.DivideByCount(4, True)
        for i in params:
            pt = crv.PointAt(i)
            circ_pts.append(pt)
        edge_pts.append(circ_pts)


pole_loft = []

for list in edge_pts:
    vert_crvs = []
    for k in list:
        index_line = rg.Curve.CreateInterpolatedCurve(k[i], 3)
        vert_crvs.append(index_line)
    srf = rg.Brep.CreateFromLoft(vert_crvs, rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType(1),False)
    pole_loft.append(srf)
    


# # str_planes = []

# # for circ in poles:
# #     str_pts = []
# #     crv_length = circ.get_length()
# #     count = int(crv_length/divide_interval)
# #     params = circ.DivideByCount(pole_count, True)
# #     for i in params:
# #         pt = circ.PointAt(i)
# #         tan = circ.TangentAt(i)

        
    


# # def divide_crv(crv, divide_interval, endInc):
# #     """
# #     Function to divide a curve by closest integer multiple of length
# #     crv : input curve
# #     divide_interval : desired length of segments
# #     endInc : if you want to include the end point
    
# #     returns : list of points and normals"""
# #     crv_length = crv.GetLength()
# #     count = int(crv_length/divide_interval)
# #     params = crv.DivideByCount(count, endInc)
# #     points = [crv.PointAt(p) for p in params] 
# #     tangents = [crv.TangentAt(p) for p in params]
# #     normals = [rg.Vector3d.CrossProduct(t, rg.Vector3d.ZAxis) for t in tangents]
# #     return points, normals