import Rhino.Geometry as rg
import copy
import math

# def OrientPlane(plane):
#     zAxis = plane.ZAxis
#     if zAxis.Z < 0:
#         zAxis = -zAxis
#     outPlane = rg.Plane(plane.Origin, zAxis)
#     xAxis = copy.copy(outPlane.XAxis)
#     xAxis.Transform(rg.Transform.ProjectAlong(rg.Plane.WorldXY, outPlane.YAxis))
#     outPlane.Transform(rg.Transform.Rotation(outPlane.XAxis, xAxis, outPlane.Origin))
#     if outPlane.YAxis.Z < 0:
#         outPlane = rg.Plane(outPlane.Origin, -outPlane.XAxis, -outPlane.YAxis)
#     return outPlane

def OrientPlane(plane, guide):
    yPt = plane.Origin + rg.Vector3d(0,0,1)
    project = rg.Transform.ProjectAlong(plane,plane.ZAxis)
    yPt.Transform(project)
    yAxis = rg.Vector3d(yPt-plane.Origin)
    
    zAxis = plane.ZAxis
    if zAxis*guide <0: zAxis = -zAxis

    outPlane = rg.Plane(plane.Origin,-rg.Vector3d.CrossProduct(zAxis,yAxis), yAxis)
    return outPlane





planes = []
flip = False
for i in range(LayerNumber):
    for c in Curves:

        params = c.DivideByCount(DivideCount, True)
        # params = []
        # for p in theParams: params.append(p)
        # params.append(params[0])

        tempPlane = []
        for k,p in enumerate(params):
                pt0 = c.PointAt(p)
                pt1 = Brep.ClosestPoint(pt0)
                temp = rg.Plane(pt1, rg.Vector3d(pt0-pt1))

                plane = OrientPlane(temp,rg.Vector3d(rg.Point3d.Origin - temp.Origin))
                # plane = temp

                dir = rg.Vector3d(pt0-pt1)
                dir.Unitize()
                move = rg.Transform.Translation( dir*LayerHight*i)
                plane.Transform(move)

                wave = rg.Transform.Translation(plane.YAxis * math.sin((100*k)/len(params))*i*1)
                plane.Transform(wave)

                halfLength = len(params)/2
                rotation2 = rg.Transform.Rotation((((halfLength - abs(halfLength-k))/halfLength)*-math.pi), plane.Normal, plane.Origin)
                # plane.Transform(rotation2)



                tempPlane.append(plane)
        if flip : tempPlane.reverse()
        flip = not flip
        planes.extend(tempPlane)

for p in planes:
    z = p.ZAxis
    z.Unitize()
    newZ = z*Inclination + rg.Vector3d.ZAxis*(1-Inclination)
    rotation = rg.Transform.Rotation(z, newZ,p.Origin)
    p.Transform(rotation)




Planes = planes
