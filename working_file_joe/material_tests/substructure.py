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
x_axis = []
y_axis = []

for c in contours:
    cont_pts = []
    temp = []
    crv = c.ToNurbsCurve(2,5)
    params = crv.DivideByCount(pole_count, True)
    for i in params:
        pt = crv.PointAt(i)
        vec = rg.Vector3d(c.Center - pt)
        temp.append(vec)
        cont_pts.append(pt)
    y_axis.append(temp)
    pts.append(cont_pts)

poles = []
pole_crvs = []


for i in range(pole_count):
    temp = []
    pole_circ = []
    
    for j, value in enumerate(pole_graph):
        pole_center_plane = rg.Plane(pts[j][i], rg.Vector3d.CrossProduct(rg.Vector3d.ZAxis,y_axis[j][i]), y_axis[j][i])
        pole_rect= rg.Rectangle3d(pole_center_plane, pole_length*(pole_graph[j]), pole_width*(pole_graph[j])).ToNurbsCurve()
        temp.append(pole_rect)
    pole = rg.Brep.CreateFromLoft(temp, rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType(1),False)
    poles.append(pole)